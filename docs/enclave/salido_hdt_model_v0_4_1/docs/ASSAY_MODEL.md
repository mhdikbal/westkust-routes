# Hoffman–Vogel Assay Model

## Purpose

Model parallel measurements without declaring one assayer automatically correct.

## Latent-content model

For batch `b` and assayer `a`:

```text
Y[a,b] = Z[b] + alpha[a] + epsilon[a,b]
```

- `Z[b]`: latent metal content;
- `alpha[a]`: systematic assayer bias;
- `epsilon[a,b]`: observation error.

A Bayesian form is recommended:

```text
Z[b] ~ Normal(mu_z, sigma_z)
Y[a,b] ~ Normal(Z[b] + alpha[a], sigma_a)
```

## Required transformations

Keep original components:

```text
mark
lood
grein
gulden
stuiver
penning
```

Do not convert to a modern unit until the historical metrology is verified.

## Analyses

- paired difference by batch;
- absolute and percentage difference;
- weekly versus general assay;
- bias by batch weight;
- anomaly identification;
- Bland–Altman visualization after unit validation.

## OCR safety

A statistical model may flag a value as implausible. It may not silently replace the archival reading.
