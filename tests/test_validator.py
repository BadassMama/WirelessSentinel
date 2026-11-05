import pandas as pd
import pytest

from src.validator import validate_data


# A clean, synthetic wireless access point
def valid_record():
    return {
        "timestamp": "2026-11-05 14:00:00",
        "ssid": "TestNetwork",
        "bssid": "AA:BB:CC:DD:EE:FF",
        "authentication": "WPA2-Personal",
        "encryption": "CCMP",
        "signal": 85,
        "radio_type": "802.11ac",
        "channel": 36
    }


def test_valid_record_has_no_issues():
    df = pd.DataFrame([valid_record()])

    issues = validate_data(df)

    assert issues == []


def test_blank_ssid_generates_warning():
    record = valid_record()
    record["ssid"] = ""

    issues = validate_data(pd.DataFrame([record]))

    assert any(
        issue["field"] == "ssid"
        and issue["severity"] == "WARNING"
        for issue in issues
    )


def test_invalid_bssid_generates_failure():
    record = valid_record()
    record["bssid"] = "NOT-A-MAC-ADDRESS"

    issues = validate_data(pd.DataFrame([record]))

    assert any(
        issue["field"] == "bssid"
        and issue["severity"] == "FAIL"
        for issue in issues
    )


def test_signal_above_100_generates_failure():
    record = valid_record()
    record["signal"] = 150

    issues = validate_data(pd.DataFrame([record]))

    assert any(
        issue["field"] == "signal"
        and issue["severity"] == "FAIL"
        for issue in issues
    )


def test_invalid_timestamp_generates_failure():
    record = valid_record()
    record["timestamp"] = "not-a-real-date"

    issues = validate_data(pd.DataFrame([record]))

    assert any(
        issue["field"] == "timestamp"
        and issue["severity"] == "FAIL"
        for issue in issues
    )


def test_missing_channel_generates_warning():
    record = valid_record()
    record["channel"] = None

    issues = validate_data(pd.DataFrame([record]))

    assert any(
        issue["field"] == "channel"
        and issue["severity"] == "WARNING"
        for issue in issues
    )


def test_duplicate_records_generate_warnings():
    record = valid_record()
    df = pd.DataFrame([record, record])

    issues = validate_data(df)

    duplicate_issues = [
        issue for issue in issues
        if issue["field"] == "record"
    ]

    assert len(duplicate_issues) == 2
    assert all(
        issue["severity"] == "WARNING"
        for issue in duplicate_issues
    )


def test_missing_required_column_raises_error():
    df = pd.DataFrame([valid_record()])
    df = df.drop(columns=["bssid"])

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_data(df)


def test_said_column_is_supported():
    record = valid_record()
    record["said"] = record.pop("ssid")

    issues = validate_data(pd.DataFrame([record]))

    assert issues == []
