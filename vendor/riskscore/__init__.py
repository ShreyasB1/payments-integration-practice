"""riskscore 2.1: transaction risk scoring.

Vendored third-party library. Do not edit. See README.md for usage.
"""
from dataclasses import dataclass

__version__ = "2.1.0"

ALLOW = "allow"
REVIEW = "review"
BLOCK = "block"

DISPOSABLE_DOMAINS = frozenset({"mailinator.com", "tempmail.dev", "throwaway.email"})

# Approximate USD value of one minor unit, used only for scoring.
_USD_PER_MINOR = {"usd": 1.0, "eur": 1.1, "gbp": 1.25}


class RiskscoreError(Exception):
    """Raised for a malformed Transaction."""


@dataclass(frozen=True)
class Transaction:
    amount: int              # minor units
    currency: str            # lowercase ISO code
    customer_id: str
    email: str
    prior_payments: int = 0  # the customer's earlier successful payments


@dataclass(frozen=True)
class Assessment:
    score: int               # 0 to 100
    decision: str            # ALLOW, REVIEW or BLOCK
    reasons: tuple           # e.g. ("large_amount", "new_customer")


def evaluate(txn, *, review_threshold=60, block_threshold=85):
    """Score a transaction and return an Assessment."""
    if not isinstance(txn, Transaction):
        raise RiskscoreError("evaluate() expects a riskscore.Transaction")
    if not isinstance(txn.amount, int) or txn.amount <= 0:
        raise RiskscoreError("amount must be a positive integer")
    if txn.currency not in _USD_PER_MINOR:
        raise RiskscoreError(f"unsupported currency: {txn.currency}")

    usd_minor = txn.amount * _USD_PER_MINOR[txn.currency]
    score = 0
    reasons = []

    if usd_minor >= 500_000:
        score += 50
        reasons.append("large_amount")
    elif usd_minor >= 100_000:
        score += 25
        reasons.append("elevated_amount")

    if txn.prior_payments == 0:
        score += 20
        reasons.append("new_customer")

    if txn.email.rsplit("@", 1)[-1].lower() in DISPOSABLE_DOMAINS:
        score += 30
        reasons.append("disposable_email")

    score = min(score, 100)
    if score >= block_threshold:
        decision = BLOCK
    elif score >= review_threshold:
        decision = REVIEW
    else:
        decision = ALLOW
    return Assessment(score, decision, tuple(reasons))
