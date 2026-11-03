import csv
import re
import subprocess
from datetime import datetime
from pathlib import Path

# Project locations
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
CSV_FILE = DATA_DIR / "wireless_scans.csv"


def run_wifi_scan():
    """Collect nearby Wi-Fi access point information from Windows."""

    print("\n[*] Starting wireless network scan...")

    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True,
            text=True,
            errors="replace",
            timeout=30
        )

        if result.returncode != 0:
            print("[!] Windows could not complete the Wi-Fi scan.")
            print(result.stderr)
            return []

        return parse_scan_results(result.stdout)

    except FileNotFoundError:
        print("[!] Could not find the Windows netsh utility.")
        return []

    except subprocess.TimeoutExpired:
        print("[!] Wi-Fi scan timed out.")
        return []


def parse_scan_results(output):
    """Extract SSID and individual access point information."""

    networks = []
    current_network = None
    current_bssid = None

    def save_bssid():
        if current_network and current_bssid:
            networks.append({
                **current_network,
                **current_bssid
            })

    for line in output.splitlines():

        # Start of a new wireless network
        match = re.match(r"^\s*SSID\s+\d+\s*:\s*(.*)$", line)

        if match:
            save_bssid()

            current_network = {
                "ssid": match.group(1).strip(),
                "authentication": "",
                "encryption": ""
            }

            current_bssid = None
            continue

        if current_network is None:
            continue

        # Network security information
        match = re.match(r"^\s*Authentication\s*:\s*(.*)$", line)
        if match:
            current_network["authentication"] = match.group(1).strip()
            continue

        match = re.match(r"^\s*Encryption\s*:\s*(.*)$", line)
        if match:
            current_network["encryption"] = match.group(1).strip()
            continue

        # Individual access point (BSSID)
        match = re.match(r"^\s*BSSID\s+\d+\s*:\s*(.*)$", line)

        if match:
            save_bssid()

            current_bssid = {
                "bssid": match.group(1).strip(),
                "signal": "",
                "radio_type": "",
                "channel": ""
            }
            continue

        if current_bssid is None:
            continue

        match = re.match(r"^\s*Signal\s*:\s*(.*)$", line)
        if match:
            current_bssid["signal"] = match.group(1).strip()
            continue

        match = re.match(r"^\s*Radio type\s*:\s*(.*)$", line)
        if match:
            current_bssid["radio_type"] = match.group(1).strip()
            continue

        match = re.match(r"^\s*Channel\s*:\s*(.*)$", line)
        if match:
            current_bssid["channel"] = match.group(1).strip()

    save_bssid()

    return networks


def save_results(networks):
    """Append scan results to a CSV file."""

    if not networks:
        print("[!] No access points were found.")
        return

    DATA_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    fields = [
        "timestamp",
        "ssid",
        "bssid",
        "authentication",
        "encryption",
        "signal",
        "radio_type",
        "channel"
    ]

    file_exists = CSV_FILE.exists()

    with CSV_FILE.open(
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(file, fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        for network in networks:
            writer.writerow({
                "timestamp": timestamp,
                **network
            })

    print(f"\n[+] Saved {len(networks)} access point records.")
    print(f"[+] Data saved to: {CSV_FILE}")


def display_results(networks):
    """Display a readable summary of discovered access points."""

    print("\n" + "=" * 75)
    print("WIRELESS SENTINEL - NETWORK DISCOVERY")
    print("=" * 75)

    for index, network in enumerate(networks, start=1):

        ssid = network["ssid"] or "<Hidden SSID>"

        print(f"\nAccess Point #{index}")
        print(f"  SSID:           {ssid}")
        print(f"  BSSID:          {network['bssid']}")
        print(f"  Security:       {network['authentication']}")
        print(f"  Encryption:     {network['encryption']}")
        print(f"  Signal:         {network['signal']}")
        print(f"  Radio:          {network['radio_type']}")
        print(f"  Channel:        {network['channel']}")

    print("\n" + "=" * 75)
    print(f"Total access points discovered: {len(networks)}")
    print("=" * 75)


def main():
    networks = run_wifi_scan()

    if networks:
        display_results(networks)
        save_results(networks)


if __name__ == "__main__":
    main()
