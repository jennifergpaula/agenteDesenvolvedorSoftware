"""Validation and processing for automated transaction records."""

from pydantic import BaseModel, Field, field_validator


AUTOMATION_LIMIT = 10_000.0


class HumanApprovalRequiredError(Exception):
    """Raised when a transaction requires human approval."""


class TransactionRecord(BaseModel):
    """Validated transaction metadata accepted by the automation pipeline."""

    transaction_id: str = Field(..., description="Unique transaction identifier.")
    amount: float = Field(..., gt=0, description="Transaction amount.")
    risk_score: float = Field(
        ..., ge=0.0, le=1.0, description="Calculated risk score."
    )

    @field_validator("amount")
    @classmethod
    def validate_automation_limit(cls, value: float) -> float:
        """Reject amounts above the automated processing limit."""
        if value > AUTOMATION_LIMIT:
            raise HumanApprovalRequiredError(
                f"Transaction amount {value} exceeds the automation limit "
                f"({AUTOMATION_LIMIT:.2f}); human approval is required."
            )
        return value


def process_transaction(raw_transaction: dict[str, object]) -> TransactionRecord:
    """Validate raw transaction data and return a transaction record.

    Args:
        raw_transaction: Transaction metadata received from an upstream pipeline.

    Returns:
        A validated transaction record.

    Raises:
        HumanApprovalRequiredError: If the amount exceeds the automation limit.
        pydantic.ValidationError: If the input does not match the model schema.
    """
    return TransactionRecord(**raw_transaction)