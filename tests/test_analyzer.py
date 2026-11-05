import pytest

from src.analyzer import classify_security


@pytest.mark.parametrize(
    "authentication, encryption, expected_severity, expected_category",
    [
        ("WPA3-Personal", "CCMP", "Low", "WPA3"),
        ("WPA2-Personal", "CCMP", "Low", "WPA2-AES"),
        ("WPA2-Personal", "AES", "Low", "WPA2-AES"),
        ("WPA2-Personal", "TKIP", "Medium", "WPA2-TKIP"),
        ("WPA2-Personal", "Unknown", "Medium", "WPA2"),
        ("WPA-Personal", "TKIP", "High", "WPA"),
        ("Open", "None", "High", "Open"),
        ("WEP", "WEP", "Critical", "WEP"),
        ("Unknown", "Unknown", "Unknown", "Unknown"),
        ("", "CCMP", "Unknown", "Unknown"),
    ],
)
def test_security_classification(
    authentication,
    encryption,
    expected_severity,
    expected_category,
):
    severity, category, explanation = classify_security(
        authentication, encryption
    )

    assert severity == expected_severity
    assert category == expected_category
    assert isinstance(explanation, str)
    assert explanation


def test_wep_encryption_takes_priority_over_open_authentication():
    severity, category, explanation = classify_security(
        "Open", "WEP"
    )

    assert severity == "Critical"
    assert category == "WEP"
