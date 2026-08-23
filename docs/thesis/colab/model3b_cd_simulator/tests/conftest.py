import sys
from pathlib import Path

# docs/thesis/colab (parent of the model3b_cd_simulator package) must be on
# sys.path so `import model3b_cd_simulator` resolves regardless of the
# directory pytest is invoked from.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
