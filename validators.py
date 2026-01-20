import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def validate_eval_001(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        results["checked"] += 1
        if len(df) != 5:
            results["failed"] += 1
            results["status"] = "FAIL"
            results["findings"].append(f"Expected 5 shipments, found {len(df)}")
        else:
            results["passed"] += 1

        for i, row in df.iterrows():
            results["checked"] += 1
            if row["totalWeightLbs"] != 4500:
                results["failed"] += 1
                results["status"] = "FAIL"
                results["findings"].append(
                    f"Row {i} weight {row['totalWeightLbs']} != 4500"
                )
            else:
                results["passed"] += 1
    except Exception as e:
        results["status"] = "ERROR"
        results["findings"].append(str(e))
    return results


def validate_eval_002(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        results["checked"] += 1
        if len(df) != 8:
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1

        for i, row in df.iterrows():
            results["checked"] += 1
            if not (3000 <= row["totalWeightLbs"] <= 5000):
                results["failed"] += 1
                results["status"] = "FAIL"
            else:
                results["passed"] += 1
    except Exception as e:
        results["status"] = "ERROR"
    return results


def validate_eval_003(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        if len(df) != 6:
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1

        results["checked"] += 1
        if df["totalWeightLbs"].sum() != 30000:
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1
    except Exception as e:
        results["status"] = "ERROR"
    return results


def validate_eval_004(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        if len(df) != 12:
            results["failed"] += 1
            results["status"] = "FAIL"
        for i, row in df.iterrows():
            results["checked"] += 2
            if not (4000 <= row["totalWeightLbs"] <= 5000):
                results["failed"] += 1
                results["status"] = "FAIL"
            else:
                results["passed"] += 1
            if not (2800 <= row["totalVolumeCuFt"] <= 3200):
                results["failed"] += 1
                results["status"] = "FAIL"
            else:
                results["passed"] += 1
    except:
        results["status"] = "ERROR"
    return results


def validate_eval_005(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        if len(df) != 15:
            results["failed"] += 1
            results["status"] = "FAIL"
        for i, row in df.iterrows():
            results["checked"] += 2
            if not (22 <= row["totalPalletCount"] <= 26):
                results["failed"] += 1
                results["status"] = "FAIL"
            else:
                results["passed"] += 1
            if not (1320 <= row["totalCaseCount"] <= 1560):
                results["failed"] += 1
                results["status"] = "FAIL"
            else:
                results["passed"] += 1
    except:
        results["status"] = "ERROR"
    return results


def validate_eval_006(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        if len(df) != 10:
            results["failed"] += 1
            results["status"] = "FAIL"
        for i, row in df.iterrows():
            results["checked"] += 4
            if row["totalWeightLbs"] != 5000:
                results["failed"] += 1
                results["status"] = "FAIL"
            else:
                results["passed"] += 1
            if row["totalVolumeCuFt"] != 3000:
                results["failed"] += 1
                results["status"] = "FAIL"
            else:
                results["passed"] += 1
            if row["totalPalletCount"] != 24:
                results["failed"] += 1
                results["status"] = "FAIL"
            else:
                results["passed"] += 1
            if row["totalCaseCount"] != 1440:
                results["failed"] += 1
                results["status"] = "FAIL"
            else:
                results["passed"] += 1
    except:
        results["status"] = "ERROR"
    return results


def validate_eval_007(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        if len(df) != 12:
            results["failed"] += 1
            results["status"] = "FAIL"
        windows = []
        for i, row in df.iterrows():
            d_start = pd.to_datetime(row["deliveryFromDateTime"])
            d_end = pd.to_datetime(row["deliveryToDateTime"])
            duration = (d_end - d_start).total_seconds() / 3600

            results["checked"] += 1
            if not (1.9 <= duration <= 2.1):
                results["failed"] += 1
                results["status"] = "FAIL"
                results["findings"].append(f"Row {i} dur {duration}")
            else:
                results["passed"] += 1

            results["checked"] += 1
            if d_start.hour not in [6, 9, 12, 15, 18]:
                results["failed"] += 1
                results["status"] = "FAIL"
            else:
                results["passed"] += 1

            windows.append((d_start, d_end))

        # Overlap
        results["checked"] += 1
        windows.sort()
        overlap = False
        for k in range(len(windows) - 1):
            if windows[k][1] > windows[k + 1][0]:
                overlap = True
        if overlap:
            results["failed"] += 1
            results["status"] = "FAIL"
            results["findings"].append("Overlap")
        else:
            results["passed"] += 1
    except Exception as e:
        results["status"] = "ERROR"
        results["findings"].append(str(e))
    return results


def validate_eval_008(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        if len(df) != 15:
            results["failed"] += 1
        weights = df["totalWeightLbs"].tolist()

        results["checked"] += 1
        if sum(weights) != 90000:
            results["failed"] += 1
            results["status"] = "FAIL"
            results["findings"].append(f"Sum {sum(weights)}")
        else:
            results["passed"] += 1

        for w in weights:
            if w % 500 != 0:
                results["failed"] += 1
                results["status"] = "FAIL"

        results["checked"] += 1
        if not (1100 <= np.std(weights) <= 1300):
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1

        results["checked"] += 1
        if len(set(weights)) != len(weights):
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1
    except Exception as e:
        results["status"] = "ERROR"
    return results


def validate_eval_009(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        if len(df) != 20:
            results["failed"] += 1
            results["status"] = "FAIL"

        tot_pal = df["totalPalletCount"].sum()
        tot_cas = df["totalCaseCount"].sum()
        tot_w = df["totalWeightLbs"].sum()
        tot_v = df["totalVolumeCuFt"].sum()

        results["checked"] += 1
        if tot_pal == 0 or abs(tot_cas / tot_pal - 60) > 0.1:
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1

        results["checked"] += 1
        if tot_v == 0 or abs(tot_w / tot_v - 1.8) > 0.1:
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1

        results["checked"] += 1
        if abs(df["totalPalletCount"].mean() - 24) > 0.5:
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1

        for w in df["totalWeightLbs"]:
            if not (5000 <= w <= 8000):
                results["failed"] += 1
                results["status"] = "FAIL"
    except Exception as e:
        results["status"] = "ERROR"
    return results


def validate_eval_010(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        if len(df) != 18:
            results["failed"] += 1
            results["status"] = "FAIL"
        w_sorted = sorted(df["totalWeightLbs"].tolist())
        diffs = [w_sorted[i + 1] - w_sorted[i] for i in range(len(w_sorted) - 1)]
        results["checked"] += 1
        if len(set(diffs)) > 1:
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1

        results["checked"] += 1
        if sum(w_sorted) != 108000:
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1
    except Exception as e:
        results["status"] = "ERROR"
    return results


def validate_eval_011(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        if len(df) != 15:
            results["failed"] += 1
        expected_pals = sorted([8, 13, 21, 34, 55] * 3)
        actual_pals = sorted(df["totalPalletCount"].tolist())

        results["checked"] += 1
        if actual_pals != expected_pals:
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1

        expected_cases = 18000
        results["checked"] += 1
        if abs(df["totalCaseCount"].sum() - 18000) > 100:
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1

    except Exception as e:
        results["status"] = "ERROR"
    return results


def validate_eval_012(df):
    results = {"status": "PASS", "findings": [], "checked": 0, "passed": 0, "failed": 0}
    try:
        df["date"] = pd.to_datetime(df["pickupFromDateTime"]).dt.date
        days = sorted(df["date"].unique())

        results["checked"] += 1
        if len(days) != 7:
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1

        daily_totals = []
        for d in days:
            day_df = df[df["date"] == d]
            if len(day_df) != 4:
                results["failed"] += 1
                results["status"] = "FAIL"

            weights = day_df["totalWeightLbs"].tolist()
            cats_found = {"L": 0, "M": 0, "H": 0, "S": 0}
            for w in weights:
                if 2000 <= w <= 3000:
                    cats_found["L"] += 1
                elif 4000 <= w <= 5000:
                    cats_found["M"] += 1
                elif 6000 <= w <= 7000:
                    cats_found["H"] += 1
                elif 8000 <= w <= 9000:
                    cats_found["S"] += 1

            if not all(v == 1 for v in cats_found.values()):
                results["failed"] += 1
                results["status"] = "FAIL"
            daily_totals.append(sum(weights))

        results["checked"] += 1
        if daily_totals != sorted(list(set(daily_totals))):
            results["failed"] += 1
            results["status"] = "FAIL"
        else:
            results["passed"] += 1
    except Exception as e:
        results["status"] = "ERROR"
        results["findings"].append(str(e))
    return results
