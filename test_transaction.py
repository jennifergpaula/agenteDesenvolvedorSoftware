import pytest
from pydantic import ValidationError

from transaction import (
    HumanApprovalRequiredError,
    TransactionRecord,
    process_transaction,
)


def test_transaction_normal() -> None:
    data = {"transaction_id": "tx_001", "amount": 1500.50, "risk_score": 0.1}

    record = process_transaction(data)

    assert record == TransactionRecord(**data)
    assert record.transaction_id == "tx_001"
    assert record.amount == 1500.50


def test_transaction_at_automation_limit_is_accepted() -> None:
    data = {"transaction_id": "tx_002", "amount": 10_000.0, "risk_score": 0.2}

    record = process_transaction(data)

    assert record.amount == 10_000.0


def test_transaction_above_limit_requires_human_approval() -> None:
    data = {"transaction_id": "tx_003", "amount": 10_000.01, "risk_score": 0.05}

    with pytest.raises(HumanApprovalRequiredError, match="human approval is required"):
        process_transaction(data)


def test_transaction_with_invalid_amount_raises_validation_error() -> None:
    data = {"transaction_id": "tx_004", "amount": -50.0, "risk_score": 0.1}

    with pytest.raises(ValidationError):
        process_transaction(data)