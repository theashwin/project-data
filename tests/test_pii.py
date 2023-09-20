import pytest
from services.user_logins import *
from unittest.mock import MagicMock, patch


def test_postgres_insert():
    records = []

    data = [{
            "user_id": "123",
            "device_type": "android",
            "ip": "1.1.1.1",
            "device_id": "1234",
            "locale": "en",
            "app_version": "1.1",
            "date": "2022-01-01"
        }]

    for message in data:
        record = create_record(message)
        records.append(record)

    assert records[0].masked_ip == "f1412386aa8db2579aff2636cb9511cacc5fd9880ecab60c048508fbe26ee4d9"
    assert records[0].masked_device_id == "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
