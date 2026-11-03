# WirelessSentinel
Python Wireless Security Analyzer
Wireless Sentinel

A Python-based wireless network discovery and security analysis tool.


Overview

Wireless Sentinel is a cybersecurity portfolio project designed to explore wireless network discovery, security configuration analysis, and automated reporting.

The project uses Python and Windows' built-in WLAN utilities to collect information about nearby wireless access points and evaluate their advertised security configurations.

The long-term goal is to develop a wireless security monitoring tool with historical tracking, anomaly detection, and an interactive dashboard.


Current Features

Discover nearby wireless networks.

Collect SSIDs and BSSIDs.

Record signal strength and wireless channels.

Identify advertised authentication and encryption configurations.

Classify WPA2, WPA3, WPA, WEP, and open network configurations.

Generate CSV-based security reports.


Technology Stack

Python 3.13

Pandas

Windows WLAN utilities (netsh)

CSV data storage

Streamlit and Plotly (planned dashboard components)


Planned Features

Interactive wireless monitoring dashboard.

Historical scan storage using SQLite.

Channel congestion analysis.

Detection of unexpected access points.

Wireless security anomaly detection.

Monitor-mode packet capture integration.

Detailed security assessment reports.



Security and Ethical Use

Wireless Sentinel is intended for educational purposes and authorized wireless security research.

The tool currently performs passive discovery using Windows WLAN utilities. Its findings describe advertised wireless configurations and should not be interpreted as proof that a network is vulnerable or compromised.

Always respect network ownership, privacy, and applicable laws when conducting wireless security research.

Project Status

Early development — Phase 1 and Phase 2 completed.
