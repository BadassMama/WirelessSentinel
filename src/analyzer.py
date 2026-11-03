import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_DIR / "data" / "wireless_scans.csv"


def classify_security(authentication, encryption):
    """Evaluate advertised wireless security settings."""

    auth = str(authentication).upper()
    cipher = str(encryption).upper()

    if not auth or auth == "NAN":
        return "Unknown", "Unknown", "Authentication information missing"

    if "OPEN" in auth or "NONE" in cipher:
        return "High", "Open", "No Wi-Fi encryption advertised"

    if "WEP" in auth or "WEP" in cipher:
        return "Critical", "WEP", "Outdated and insecure encryption"

    if "WPA3" in auth:
        return "Low", "WPA3", "Modern wireless security advertised"

    if "WPA2" in auth:
        if "TKIP" in cipher:
            return "Medium", "WPA2-TKIP", "Legacy cipher detected"

        if "CCMP" in cipher or "AES" in cipher:
            return "Low", "WPA2-AES", "Modern WPA2 encryption advertised"

        return "Medium", "WPA2", "Review encryption configuration"

    if "WPA" in auth:
        return "High", "WPA", "Legacy WPA security detected"

    return "Unknown", "Unknown", "Unrecognized security configuration"


def analyze_networks():
    """Read collected scans and evaluate wireless security."""

    if not CSV_FILE.exists():
        print("[!] No scan data found.")
        return

    df = pd.read_csv(CSV_FILE)

    if df.empty:
        print("[!] Scan file is empty.")
        return

    findings = []

    for _, row in df.iterrows():

        severity, category, explanation = classify_security(
            row["authentication"],
            row["encryption"]
        )

        findings.append({
            "SSID": row["ssid"],
            "BSSID": row["bssid"],
            "Authentication": row["authentication"],
            "Encryption": row["encryption"],
            "Severity": severity,
            "Classification": category,
            "Finding": explanation
        })

    results = pd.DataFrame(findings)

    print("\n" + "=" * 75)
    print("WIRELESS SENTINEL - SECURITY ANALYSIS")
    print("=" * 75)

    print(results.to_string(index=False))

    print("\n" + "=" * 75)
    print("FINDINGS SUMMARY")
    print("=" * 75)

    print(results["Severity"].value_counts().to_string())

    report_path = PROJECT_DIR / "reports" / "security_report.csv"

    report_path.parent.mkdir(exist_ok=True)
    results.to_csv(report_path, index=False)

    print(f"\n[+] Security report saved to: {report_path}")


if __name__ == "__main__":
    analyze_networks()