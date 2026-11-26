from dataclasses import dataclass, field


@dataclass
class Customer:
    id: str
    email: str


@dataclass
class PaymentIntent:
    id: str
    customer_id: str
    amount: int                  # minor units, e.g. cents
    currency: str                # lowercase ISO code, e.g. "usd"
    status: str = "requires_confirmation"
    metadata: dict = field(default_factory=dict)
