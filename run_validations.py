import os
import pandas as pd
from validators import (
    validate_eval_001,
    validate_eval_002,
    validate_eval_003,
    validate_eval_004,
    validate_eval_005,
    validate_eval_006,
    validate_eval_007,
    validate_eval_008,
    validate_eval_009,
    validate_eval_010,
    validate_eval_011,
    validate_eval_012,
)
from datetime import datetime

VALIDATORS = {
    "EVAL-001": validate_eval_001,
    "EVAL-002": validate_eval_002,
    "EVAL-003": validate_eval_003,
    "EVAL-004": validate_eval_004,
    "EVAL-005": validate_eval_005,
    "EVAL-006": validate_eval_006,
    "EVAL-007": validate_eval_007,
    "EVAL-008": validate_eval_008,
    "EVAL-009": validate_eval_009,
    "EVAL-010": validate_eval_010,
    "EVAL-011": validate_eval_011,
    "EVAL-012": validate_eval_012,
}


def main():
    results_list = []

    # Read Eval Set to get prompts
    try:
        eval_meta = pd.read_csv("references/Eval_set.csv")
    except:
        print("Could not read references/Eval_set.csv")
        return

    for index, row in eval_meta.iterrows():
        eval_id = f"EVAL-{str(row['#']).zfill(3)}"
        user_prompt = row["User Prompt"]
        file_path = os.path.join("generated_data", f"{eval_id}_Output.xlsx")

        entry = {
            "Eval_Set_ID": eval_id,
            "User_Prompt": user_prompt,
            "Status": "NOT RUN",
            "Total_Checks": 0,
            "Passed_Checks": 0,
            "Failed_Checks": 0,
            "Findings": "",
            "Validated_By": "Antigravity",
            "Timestamp": datetime.now().isoformat(),
        }

        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path)
                validator = VALIDATORS.get(eval_id)
                if validator:
                    val_res = validator(df)
                    entry["Status"] = val_res["status"]
                    entry["Total_Checks"] = val_res["checked"]
                    entry["Passed_Checks"] = val_res["passed"]
                    entry["Failed_Checks"] = val_res["failed"]
                    entry["Findings"] = "; ".join(val_res["findings"])
                else:
                    entry["Findings"] = "Validator not implemented"
            except Exception as e:
                entry["Status"] = "ERROR"
                entry["Findings"] = str(e)
        else:
            entry["Status"] = "MISSING"
            entry["Findings"] = "Output file not found"

        results_list.append(entry)

    # Save Results
    results_df = pd.DataFrame(results_list)
    results_df.to_excel("Eval_result.xlsx", index=False)
    print("Validation complete. Results saved to Eval_result.xlsx")


if __name__ == "__main__":
    main()
