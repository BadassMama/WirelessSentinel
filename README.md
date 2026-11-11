\# Wireless Sentinel



\[!\[Wireless Sentinel Tests](https://github.com/BadassMama/WirelessSentinel/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/BadassMama/WirelessSentinel/actions/workflows/tests.yml)



\*\*A Python-based Wi-Fi discovery, security configuration analysis, and data-quality monitoring project for Windows.\*\*



Wireless Sentinel collects information advertised by nearby wireless access points using Windows' built-in WLAN tools, classifies common security configurations, validates collected records, and presents findings in an interactive dashboard. It is designed as a hands-on cybersecurity engineering and defensive analysis project, not an exploitation tool.



\## Highlights



\- \*\*Wireless discovery:\*\* Collect SSIDs, BSSIDs, signal strength, channels, radio types, authentication methods, and encryption types using `netsh`.

\- \*\*Security configuration analysis:\*\* Assign an initial risk category to open, WEP, WPA, WPA2, and WPA3 configurations and export CSV findings.

\- \*\*Data quality checks:\*\* Detect invalid timestamps, malformed BSSIDs, out-of-range signal and channel values, missing fields, and duplicate records. Blank SSIDs are flagged for review rather than automatically treated as errors.

\- \*\*Interactive dashboard:\*\* Explore scan records, security categories, signal strength, and channel distribution with Streamlit and Plotly.

\- \*\*Automated testing:\*\* Use 20 `pytest` cases to verify validation rules and security classification, including a regression test for WEP classification precedence.

\- \*\*Continuous integration:\*\* Run the unit tests on GitHub Actions for pushes and pull requests targeting `main`.



\## Technology



Python 3.13 · pandas · Streamlit · Plotly · pytest · Windows `netsh` · GitHub Actions · CSV



\## Project structure



```text

WirelessSentinel/

├── .github/

│   └── workflows/

│       └── tests.yml

├── src/

│   ├── scanner.py

│   ├── analyzer.py

│   ├── validator.py

│   └── dashboard.py

├── tests/

│   ├── test\_analyzer.py

│   └── test\_validator.py

├── data/                       # Local scan output (not committed)

├── reports/                    # Generated reports (not committed)

├── requirements.txt

└── README.md

```



\## Getting started



\*\*Prerequisites:\*\* Windows with a functioning Wi-Fi adapter, Python 3.13, and PowerShell. Live wireless discovery uses Windows `netsh` and is not supported by this scanner on other operating systems.



Clone the repository and open the project folder:



```powershell

git clone https://github.com/BadassMama/WirelessSentinel.git

cd WirelessSentinel

```



Create and activate an isolated Python environment:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



If PowerShell blocks activation, you can allow it \*\*for the current session only\*\*:



```powershell

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\\.venv\\Scripts\\Activate.ps1

```



Install project dependencies:



```powershell

python -m pip install -r requirements.txt

```



Collect a wireless scan:



```powershell

python src/scanner.py

```



Analyze and validate the collected data:



```powershell

python src/analyzer.py

python src/validator.py

```



Launch the interactive dashboard:



```powershell

streamlit run src/dashboard.py

```



> \*\*Note:\*\* The scanner must generate `data/wireless\_scans.csv` before the analyzer, validator, or dashboard can use scan data. The `data/` and `reports/` folders contain local or generated artifacts and are excluded from version control.



\## Security classification



Wireless Sentinel classifies \*advertised configurations\* using the following initial rules:



| Advertised configuration | Classification | Initial risk |

| --- | --- | --- |

| WPA3 | WPA3 | Low |

| WPA2 with AES/CCMP | WPA2-AES | Low |

| WPA2 with TKIP | WPA2-TKIP | Medium |

| WPA2 with unspecified/other cipher | WPA2 | Medium |

| Legacy WPA | WPA | High |

| Open/no encryption | Open | High |

| WEP | WEP | Critical |

| Unrecognized or missing authentication | Unknown | Unknown |



WEP detection takes precedence when a scan reports an unusual combination such as `Open` authentication with `WEP` encryption. This edge case was identified and verified through an automated regression test.



\*\*Important:\*\* These labels are heuristics, not a complete security assessment. WPA3 or WPA2-AES does not guarantee a secure network; an open network is not automatically malicious. Results depend on what Windows reports and do not establish whether an access point is compromised.



\## Data quality and testing



The validator records `FAIL` and `WARNING` findings without changing the underlying scan file. For example, malformed BSSIDs and invalid timestamps are failures; a blank SSID can be a legitimate hidden network and is treated as a warning.



Run the test suite locally:



```powershell

python -m pip install pytest

python -m pytest -v

```



The 20 test cases cover valid and malformed scan records, duplicate detection, missing required fields, legacy-column handling, and security classification edge cases. The GitHub Actions workflow runs these tests in a clean Python 3.13 environment, independently of a physical Wi-Fi adapter.



\[View the automated test workflow](https://github.com/BadassMama/WirelessSentinel/actions/workflows/tests.yml)



\## Current limitations



\- Windows-focused network discovery through `netsh`; no monitor-mode packet capture.

\- Classification uses advertised authentication and encryption settings rather than active vulnerability testing.

\- CSV-based local storage; SQLite and advanced historical analysis are not yet implemented.

\- Wireless scanning behavior depends on the adapter, drivers, and Windows' available scan results.



\## Roadmap



\- \[ ] Add historical trend analysis and optional SQLite storage.

\- \[ ] Improve channel-usage and congestion visualizations.

\- \[ ] Add tests covering the end-to-end scan-to-report flow.

\- \[ ] Expand anomaly detection for changes in observed access points.

\- \[ ] Explore optional monitor-mode support with compatible hardware in an authorized lab.



\## Security and ethical use



Wireless Sentinel is intended for learning, defensive visibility, and authorized wireless security research. It collects network information that nearby access points advertise; it does not attempt to authenticate to networks, capture user traffic, or exploit devices. Only assess networks and environments you own or have explicit permission to test. Avoid publishing scan files containing other people's SSIDs, BSSIDs, or location-related details.



\## Why I built it



I built Wireless Sentinel to strengthen my practical skills in Python, wireless security fundamentals, data validation, software testing, and CI. The project emphasizes not just detecting potentially weak configurations, but also checking whether the underlying data is trustworthy and preventing regressions as the code evolves.



\---



\*\*Project status:\*\* Working portfolio project under active development.

