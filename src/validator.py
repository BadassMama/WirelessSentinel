import pandas as pd
import re
from pathlib import Path

# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_ROOT / "data" / "wireless_scans.csv"
REPORT_FILE = PROJECT_ROOT / "reports" / "data_quality_report.csv"

REQUIRED_COLUMNS = [
    "timestamp",
    "ssid",
    "bssid",
    "authentication",
    "encryption",
    "signal",
    "radio_type",
    "channel"
]

# --------------------------------------------------
# Validation functions
# --------------------------------------------------

def add_issue(issues, row, field, severity, message):
    issues.append({
        "row": row,
        "field": field,
        "severity": severity,
        "message": message
    })


def validate_data(df):

    issues = []

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Support the existing scanner's "said" column
    if "ssid" not in df.columns and "said" in df.columns:
        df = df.rename(columns={"said": "ssid"})

    # Check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Check every record
    for index, row in df.iterrows():

        # CSV line number (header is line 1)
        row_number = index + 2

        # Timestamp
        timestamp = pd.to_datetime(
            row["timestamp"], errors="coerce"
        )

        if pd.isna(timestamp):
            add_issue(
                issues, row_number, "timestamp",
                "FAIL", "Invalid or missing timestamp"
            )

        # SSID
        if pd.isna(row["ssid"]) or str(row["ssid"]).strip() == "":
            add_issue(
                issues, row_number, "ssid",
                "WARNING", "SSID is blank; this may be a hidden network"
            )

        # BSSID
        bssid = str(row["bssid"]).strip()

        if (
            pd.isna(row["bssid"])
            or not re.fullmatch(
                r"(?i)([0-9a-f]{2}:){5}[0-9a-f]{2}", bssid
            )
        ):
            add_issue(
                issues, row_number, "bssid",
                "FAIL", "Missing or invalid MAC address format"
            )

        # Signal strength
        signal = pd.to_numeric(
            str(row["signal"]).replace("%", ""),
            errors="coerce"
        )

        if pd.isna(signal):
            add_issue(
                issues, row_number, "signal",
                "WARNING", "Signal strength is missing or non-numeric"
            )
        elif not 0 <= signal <= 100:
            add_issue(
                issues, row_number, "signal",
                "FAIL", "Signal strength must be between 0 and 100"
            )

        # Channel
        channel = pd.to_numeric(
            row["channel"], errors="coerce"
        )

        if pd.isna(channel):
            add_issue(
                issues, row_number, "channel",
                "WARNING", "Channel is missing or non-numeric"
            )
        elif (
            not float(channel).is_integer()
            or not 1 <= channel <= 233
        ):
            add_issue(
                issues, row_number, "channel",
                "FAIL", "Channel must be an integer from 1 to 233"
            )

        # Authentication
        if (
            pd.isna(row["authentication"])
            or str(row["authentication"]).strip() == ""
        ):
            add_issue(
                issues, row_number, "authentication",
                "WARNING", "Authentication information is missing"
            )

        # Encryption
        if (
            pd.isna(row["encryption"])
            or str(row["encryption"]).strip() == ""
        ):
            add_issue(
                issues, row_number, "encryption",
                "WARNING", "Encryption information is missing"
            )

        # Radio type
        if (
            pd.isna(row["radio_type"])
            or str(row["radio_type"]).strip() == ""
        ):
            add_issue(
                issues, row_number, "radio_type",
                "WARNING", "Radio type is missing"
            )

    # Exact duplicate records
    duplicates = df.duplicated(keep=False)

    for index in df[duplicates].index:
        add_issue(
            issues, index + 2, "record",
            "WARNING", "Exact duplicate record detected"
        )

    return issues


# --------------------------------------------------
# Run validator
# --------------------------------------------------

def main():

    print("\nWireless Sentinel - Data Quality Validator")
    print("-" * 45)

    if not CSV_FILE.exists():
        print("ERROR: Scan CSV file not found.")
        return

    try:
        df = pd.read_csv(CSV_FILE)

        if df.empty:
            print("ERROR: Scan CSV contains no records.")
            return

        issues = validate_data(df)

    except (ValueError, pd.errors.EmptyDataError) as error:
        print(f"VALIDATION ERROR: {error}")
        return

    # Summarize results
    total_records = len(df)

    fail_count = sum(
        issue["severity"] == "FAIL" for issue in issues
    )

    warning_count = sum(
        issue["severity"] == "WARNING" for issue in issues
    )

    passed_records = total_records - len({
        issue["row"] for issue in issues
        if issue["severity"] == "FAIL"
    })

    print(f"\nRecords examined: {total_records}")
    print(f"Records without FAIL issues: {passed_records}")
    print(f"FAIL issues: {fail_count}")
    print(f"WARNING issues: {warning_count}")

    # Save detailed report
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    report = pd.DataFrame(
        issues,
        columns=["row", "field", "severity", "message"]
    )

    report.to_csv(REPORT_FILE, index=False)

    if issues:
        print("\nIssues detected:")

        for issue in issues[:20]:
            print(
                f"[{issue['severity']}] "
                f"Row {issue['row']} - "
                f"{issue['field']}: {issue['message']}"
            )

        if len(issues) > 20:
            print(f"\n...and {len(issues) - 20} more issues.")

    else:
        print("\nPASS: No data quality issues detected.")

    print(f"\nReport saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()