"""Statistical instrumentation layered on top of the unchanged, audited
point-estimation code (`estimate.py`, `likelihood.py`). Covariance/SE/CI,
a boundary-aware likelihood-ratio test for `alpha=0`, branching-ratio
uncertainty via the delta method, AIC/BIC, and three-model (M1/M2/M3B-CD)
comparison — none of it modifies `estimate.py` or `likelihood.py`.

Every function here composes existing, unchanged building blocks:
`estimate.fit_m1/fit_m2/fit_m3b_cd` for point estimates,
`likelihood.loglik_m1/loglik_m2/loglik_m3b_cd` for the objective, and
`hessian.finite_difference_hessian` for curvature.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.stats import chi2

from .estimate import _EPS, fit_m1, fit_m2, fit_m3b_cd
from .hessian import HessianDiagnostics, finite_difference_hessian
from .likelihood import loglik_m1, loglik_m2, loglik_m3b_cd
from .schema import FitResult

_SINGULAR_CONDITION_CEILING = 1e10
COVARIANCE_STATUSES = ("valid", "regularized", "singular", "non_positive_definite", "unavailable")


@dataclass
class CovarianceResult:
    param_names: list[str]
    status: str  # one of COVARIANCE_STATUSES
    covariance: np.ndarray | None
    diagnostics: HessianDiagnostics | None
    regularization_added: float | None = None
    error_message: str = ""

    def __post_init__(self) -> None:
        if self.status not in COVARIANCE_STATUSES:
            raise ValueError(f"status must be one of {COVARIANCE_STATUSES}, got {self.status!r}")


def covariance_from_neg_loglik(
    neg_loglik: Callable[[np.ndarray], float],
    x_hat: np.ndarray,
    param_names: list[str],
    *,
    lower_bounds: np.ndarray | None = None,
    upper_bounds: np.ndarray | None = None,
) -> CovarianceResult:
    """covariance = inverse(Hessian of the NEGATIVE log-likelihood) at the MLE.

    Never silently reports "valid" just because a matrix inversion
    succeeded numerically -- symmetry, finiteness, positive-definiteness,
    minimum eigenvalue, and condition number are all checked first, and
    `status` reflects exactly which of those checks passed. A ridge
    regularization repair (for mild, noise-level non-PD cases) is
    recorded under its own `regularized` status, never folded into
    `valid`.
    """
    try:
        diag = finite_difference_hessian(neg_loglik, x_hat, lower_bounds=lower_bounds, upper_bounds=upper_bounds)
    except Exception as exc:  # noqa: BLE001 - any Hessian-evaluation failure is "unavailable", not a crash
        return CovarianceResult(param_names, "unavailable", None, None, error_message=f"{type(exc).__name__}: {exc}")

    H = diag.hessian_symmetrized
    if not np.all(np.isfinite(H)):
        return CovarianceResult(param_names, "unavailable", None, diag, error_message="Hessian contains nonfinite entries")

    if diag.condition_number > _SINGULAR_CONDITION_CEILING or not np.isfinite(diag.condition_number):
        return CovarianceResult(param_names, "singular", None, diag, error_message=f"condition_number={diag.condition_number:.3e} exceeds ceiling")

    if diag.is_positive_definite:
        try:
            cov = np.linalg.inv(H)
        except np.linalg.LinAlgError as exc:
            return CovarianceResult(param_names, "unavailable", None, diag, error_message=str(exc))
        if not np.all(np.isfinite(cov)):
            return CovarianceResult(param_names, "unavailable", None, diag, error_message="inverse contains nonfinite entries")
        return CovarianceResult(param_names, "valid", cov, diag)

    # not PD: distinguish noise-level (repairable via ridge) from genuinely non-PD
    max_abs_eig = max(abs(diag.max_eigenvalue), 1.0)
    if diag.min_eigenvalue > -1e-3 * max_abs_eig:
        ridge = abs(diag.min_eigenvalue) + 1e-8 * max_abs_eig
        H_reg = H + ridge * np.eye(H.shape[0])
        try:
            cov = np.linalg.inv(H_reg)
        except np.linalg.LinAlgError as exc:
            return CovarianceResult(param_names, "unavailable", None, diag, error_message=str(exc))
        if not np.all(np.isfinite(cov)):
            return CovarianceResult(param_names, "unavailable", None, diag, error_message="regularized inverse nonfinite")
        return CovarianceResult(param_names, "regularized", cov, diag, regularization_added=ridge)

    return CovarianceResult(param_names, "non_positive_definite", None, diag, error_message=f"min_eigenvalue={diag.min_eigenvalue:.3e}")


def standard_errors(cov: CovarianceResult) -> dict[str, float]:
    """sqrt(diag(covariance)); NaN for every parameter when covariance is unavailable."""
    if cov.covariance is None:
        return {name: float("nan") for name in cov.param_names}
    diag = np.diag(cov.covariance)
    return {name: (float(math.sqrt(v)) if v >= 0 else float("nan")) for name, v in zip(cov.param_names, diag.tolist())}


def wald_ci_95(estimate: float, se: float) -> tuple[float, float]:
    """estimate +/- 1.96*se. Valid for interior parameters under standard
    asymptotics. NOT valid for testing alpha=0 near its boundary -- use
    `boundary_aware_alpha_test` for that (asymptotic normality breaks down
    at a boundary of the parameter space). Returns (nan, nan) if se is nan."""
    if not math.isfinite(se):
        return (float("nan"), float("nan"))
    return (estimate - 1.96 * se, estimate + 1.96 * se)


# --------------------------------------------------------------------------
# Boundary-aware alpha=0 test: Self & Liang (1987) 50:50 chi-square mixture
# --------------------------------------------------------------------------


@dataclass
class BoundaryAlphaTest:
    test_statistic_lr: float
    reference_distribution: str
    p_value: float
    decision_alpha_0p05: str  # "reject_H0" | "fail_to_reject_H0"
    alpha_hat: float
    at_boundary: bool
    restricted_model: str
    unrestricted_model: str
    loglik_restricted: float
    loglik_unrestricted: float
    note: str = (
        "This is a likelihood-ratio test with null alpha=0, NOT a Wald test. "
        "Because alpha=0 is on the boundary of the parameter space [0, inf), "
        "the classical chi-square_1 null distribution does not apply; the "
        "correct asymptotic null distribution here is the Self & Liang (1987) "
        "50:50 mixture of a point mass at 0 and chi-square_1."
    )


def boundary_aware_alpha_test(
    loglik_unrestricted: float,
    loglik_restricted: float,
    alpha_hat: float,
    at_boundary: bool,
    *,
    restricted_model: str,
    unrestricted_model: str,
) -> BoundaryAlphaTest:
    """Likelihood-ratio test of H0: alpha=0 vs H1: alpha>0, using the
    boundary-corrected 50:50 chi-square_0/chi-square_1 mixture null
    distribution (Self & Liang 1987) instead of a plain Wald CI-on-zero
    check or a naive chi-square_1 LR test.

    LR = 2*(loglik_unrestricted - loglik_restricted).
    p_value = 0.5 * P(chi-square_1 >= LR) for LR > 0; = 1.0 for LR <= 0
    (LR<=0 can occur numerically when alpha_hat==0 exactly, i.e. the
    unrestricted fit already collapsed to the restricted model -- no
    evidence against H0 in that case, by construction).
    """
    lr = 2.0 * (loglik_unrestricted - loglik_restricted)
    if lr <= 0:
        p_value = 1.0
        lr = max(lr, 0.0)  # report the clipped, non-negative statistic; do not hide a negative raw LR
    else:
        p_value = 0.5 * float(chi2.sf(lr, df=1))
    decision = "reject_H0" if p_value < 0.05 else "fail_to_reject_H0"
    return BoundaryAlphaTest(
        test_statistic_lr=lr,
        reference_distribution="0.5 * point_mass(0) + 0.5 * chi_square(df=1)  [Self & Liang 1987]",
        p_value=p_value,
        decision_alpha_0p05=decision,
        alpha_hat=alpha_hat,
        at_boundary=at_boundary,
        restricted_model=restricted_model,
        unrestricted_model=unrestricted_model,
        loglik_restricted=loglik_restricted,
        loglik_unrestricted=loglik_unrestricted,
    )


# --------------------------------------------------------------------------
# Branching-ratio uncertainty via the delta method
# --------------------------------------------------------------------------


@dataclass
class BranchingRatioUncertainty:
    branching_ratio: float
    branching_ratio_standard_error: float | str
    branching_ratio_ci_95: tuple[float, float] | str
    delta_method_status: str  # "computed" | "unavailable"


def branching_ratio_delta_method(alpha_hat: float, beta_hat: float, cov: CovarianceResult, alpha_idx: int, beta_idx: int) -> BranchingRatioUncertainty:
    """n = alpha/beta. Delta method: Var(n) ~= g^T Sigma g,
    g = [dn/dalpha, dn/dbeta] = [1/beta, -alpha/beta^2].
    Only available when the (alpha, beta) block of the covariance matrix
    is valid (status in {"valid", "regularized"}) -- otherwise explicitly
    "unavailable", never silently substituted.
    """
    n_hat = alpha_hat / beta_hat
    if cov.covariance is None or cov.status not in ("valid", "regularized"):
        return BranchingRatioUncertainty(n_hat, "unavailable", "unavailable", "unavailable")

    g = np.array([1.0 / beta_hat, -alpha_hat / beta_hat**2])
    sub_cov = cov.covariance[np.ix_([alpha_idx, beta_idx], [alpha_idx, beta_idx])]
    var_n = float(g @ sub_cov @ g)
    if not math.isfinite(var_n) or var_n < 0:
        return BranchingRatioUncertainty(n_hat, "unavailable", "unavailable", "unavailable")
    se_n = math.sqrt(var_n)
    return BranchingRatioUncertainty(n_hat, se_n, wald_ci_95(n_hat, se_n), "computed")


# --------------------------------------------------------------------------
# AIC / BIC
# --------------------------------------------------------------------------


def aic(loglik: float, k: int) -> float:
    return 2 * k - 2 * loglik


def bic(loglik: float, k: int, n_bic: int) -> float:
    """n_BIC = number of events in the fitted sequence (documented
    convention, applied identically to M1, M2, and M3B-CD on the same
    event sequence -- each event contributes one likelihood factor to a
    point-process likelihood, making event count the natural point-process
    "sample size", unlike an i.i.d.-sample BIC). n_BIC=0 is clamped to 1
    (ln(0) undefined) with the clamp visible to the caller via the
    returned tuple's second element being False."""
    n_eff = max(n_bic, 1)
    return k * math.log(n_eff) - 2 * loglik


# --------------------------------------------------------------------------
# Full model-fit report: point estimate + inference, per model
# --------------------------------------------------------------------------


@dataclass
class ModelFitReport:
    model: str
    fit: FitResult
    n_bic: int
    n_bic_clamped: bool
    param_names: list[str]
    covariance: CovarianceResult
    standard_errors: dict[str, float]
    wald_ci_95: dict[str, tuple[float, float]]
    aic: float
    bic: float
    boundary_alpha_test: BoundaryAlphaTest | None = None
    branching_ratio: BranchingRatioUncertainty | None = None


def _wald_ci_for_all(fit: FitResult, se: dict[str, float]) -> dict[str, tuple[float, float]]:
    return {name: wald_ci_95(fit.params[name], se[name]) for name in fit.params}


def fit_m1_with_inference(events: np.ndarray, t0: float, t1: float, x0=None) -> ModelFitReport:
    events = np.asarray(events, dtype=float)
    fit = fit_m1(events, t0, t1, x0=x0)
    names = ["mu", "alpha", "beta"]
    x_hat = np.array([fit.params[n] for n in names])

    def neg_ll(x):
        mu, alpha, beta = x
        try:
            return -loglik_m1(events, mu, alpha, beta, t0, t1)
        except ValueError:
            return math.inf

    cov = covariance_from_neg_loglik(neg_ll, x_hat, names, lower_bounds=np.array([_EPS, 0.0, _EPS]), upper_bounds=None)
    se = standard_errors(cov)

    # restricted model (alpha=0): closed-form homogeneous Poisson, mu_hat = n/(t1-t0)
    n_events = events.size
    mu_restricted = n_events / (t1 - t0)
    loglik_restricted = n_events * math.log(mu_restricted) - mu_restricted * (t1 - t0) if mu_restricted > 0 else float("-inf")
    boundary_test = boundary_aware_alpha_test(
        fit.loglik, loglik_restricted, fit.params["alpha"], fit.boundary_flags.get("alpha", False),
        restricted_model="homogeneous_poisson(mu=n/(t1-t0))", unrestricted_model="m1",
    )
    br = branching_ratio_delta_method(fit.params["alpha"], fit.params["beta"], cov, names.index("alpha"), names.index("beta"))

    n_bic = n_events
    return ModelFitReport(
        model="m1", fit=fit, n_bic=n_bic, n_bic_clamped=(n_bic == 0), param_names=names,
        covariance=cov, standard_errors=se, wald_ci_95=_wald_ci_for_all(fit, se),
        aic=aic(fit.loglik, len(names)), bic=bic(fit.loglik, len(names), n_bic),
        boundary_alpha_test=boundary_test, branching_ratio=br,
    )


def fit_m2_with_inference(events: np.ndarray, year_covariates: dict[int, float], t0: float, t1: float, x0=None) -> ModelFitReport:
    events = np.asarray(events, dtype=float)
    fit = fit_m2(events, year_covariates, t0, t1, x0=x0)
    names = ["theta0", "theta1"]
    x_hat = np.array([fit.params[n] for n in names])

    def neg_ll(x):
        theta0, theta1 = x
        try:
            return -loglik_m2(events, theta0, theta1, year_covariates, t0, t1)
        except ValueError:
            return math.inf

    cov = covariance_from_neg_loglik(neg_ll, x_hat, names)
    se = standard_errors(cov)
    n_bic = events.size
    return ModelFitReport(
        model="m2", fit=fit, n_bic=n_bic, n_bic_clamped=(n_bic == 0), param_names=names,
        covariance=cov, standard_errors=se, wald_ci_95=_wald_ci_for_all(fit, se),
        aic=aic(fit.loglik, len(names)), bic=bic(fit.loglik, len(names), n_bic),
    )


def fit_m3b_cd_with_inference(events: np.ndarray, year_covariates: dict[int, float], t0: float, t1: float, x0=None) -> ModelFitReport:
    events = np.asarray(events, dtype=float)
    fit = fit_m3b_cd(events, year_covariates, t0, t1, x0=x0)
    names = ["theta0", "theta1", "alpha", "beta"]
    x_hat = np.array([fit.params[n] for n in names])

    def neg_ll(x):
        theta0, theta1, alpha, beta = x
        try:
            return -loglik_m3b_cd(events, theta0, theta1, alpha, beta, year_covariates, t0, t1)
        except ValueError:
            return math.inf

    lower = np.array([-np.inf, -np.inf, 0.0, _EPS])
    cov = covariance_from_neg_loglik(neg_ll, x_hat, names, lower_bounds=lower, upper_bounds=None)
    se = standard_errors(cov)

    # restricted model (alpha=0) = M2 with the same theta0/theta1 starting point re-fit
    restricted = fit_m2(events, year_covariates, t0, t1)
    boundary_test = boundary_aware_alpha_test(
        fit.loglik, restricted.loglik, fit.params["alpha"], fit.boundary_flags.get("alpha", False),
        restricted_model="m2", unrestricted_model="m3b_cd",
    )
    br = branching_ratio_delta_method(fit.params["alpha"], fit.params["beta"], cov, names.index("alpha"), names.index("beta"))

    n_bic = events.size
    return ModelFitReport(
        model="m3b_cd", fit=fit, n_bic=n_bic, n_bic_clamped=(n_bic == 0), param_names=names,
        covariance=cov, standard_errors=se, wald_ci_95=_wald_ci_for_all(fit, se),
        aic=aic(fit.loglik, len(names)), bic=bic(fit.loglik, len(names), n_bic),
        boundary_alpha_test=boundary_test, branching_ratio=br,
    )


# --------------------------------------------------------------------------
# Model selection summary
# --------------------------------------------------------------------------


@dataclass
class ModelSelectionSummary:
    best_model_by_AIC: str
    best_model_by_BIC: str
    delta_AIC: dict[str, float]
    delta_BIC: dict[str, float]
    caveat: str = (
        "Model selection here reflects goodness of fit to ONE event sequence "
        "under this pilot's simulator; it is a pipeline-verification result, "
        "not a claim about historical process, causal mechanism, or which "
        "model 'actually generated' any real data."
    )


def select_best_model(reports: dict[str, ModelFitReport]) -> ModelSelectionSummary:
    aics = {name: r.aic for name, r in reports.items()}
    bics = {name: r.bic for name, r in reports.items()}
    best_aic = min(aics, key=aics.get)
    best_bic = min(bics, key=bics.get)
    return ModelSelectionSummary(
        best_model_by_AIC=best_aic, best_model_by_BIC=best_bic,
        delta_AIC={name: aics[name] - aics[best_aic] for name in aics},
        delta_BIC={name: bics[name] - bics[best_bic] for name in bics},
    )
