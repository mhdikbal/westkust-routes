import json
from v2a_full_study import run_family_recovery, B
from v2a_designs import DESIGNS

recovery_rows = []
for d in ["D7", "D8", "D9", "D10"]:
    for r in range(B):
        run_family_recovery(d, r, recovery_rows)

json.dump(recovery_rows, open("v2a_full_study_recovery_rows.json", "w"), default=str)
print("rerun done, n rows:", len(recovery_rows))
