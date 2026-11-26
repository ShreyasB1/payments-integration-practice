from payments.errors import InvalidRequest, InvalidState
from payments.events import EventBus
from payments.models import Customer, PaymentIntent
from payments.store import Store

SUPPORTED_CURRENCIES = {"usd", "eur", "gbp"}


class PaymentService:
    def __init__(self, store=None, bus=None):
        self.store = store or Store()
        self.bus = bus or EventBus()

    # ---- customers ----

    def create_customer(self, email):
        if "@" not in email:
            raise InvalidRequest("email must contain @")
        customer = Customer(self.store.next_id("cus"), email)
        self.store.put("customer", customer)
        self.bus.publish("customer.created", {"id": customer.id})
        return customer

    # ---- payment intents ----

    def create_payment_intent(self, customer_id, amount, currency="usd", metadata=None):
        self.store.get("customer", customer_id)          # raises NotFound
        self._validate_amount(amount)
        currency = currency.lower()
        if currency not in SUPPORTED_CURRENCIES:
            raise InvalidRequest(f"unsupported currency: {currency}")

        intent = PaymentIntent(
            id=self.store.next_id("pi"),
            customer_id=customer_id,
            amount=amount,
            currency=currency,
            metadata=dict(metadata or {}),
        )
        self.store.put("payment_intent", intent)
        self.bus.publish("payment_intent.created", self._intent_payload(intent))
        return intent

    def confirm(self, intent_id):
        intent = self.store.get("payment_intent", intent_id)
        self._require_status(intent, "requires_confirmation")
        intent.status = "succeeded"
        self.bus.publish("payment_intent.succeeded", self._intent_payload(intent))
        return intent

    def cancel(self, intent_id):
        intent = self.store.get("payment_intent", intent_id)
        self._require_status(intent, "requires_confirmation")
        intent.status = "canceled"
        self.bus.publish("payment_intent.canceled", self._intent_payload(intent))
        return intent

    def list_payments(self, customer_id, status=None):
        return [
            intent for intent in self.store.all("payment_intent")
            if intent.customer_id == customer_id
            and (status is None or intent.status == status)
        ]

    # ---- helpers ----

    @staticmethod
    def _validate_amount(amount):
        # bool is a subclass of int in Python, so rule it out explicitly.
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            raise InvalidRequest("amount must be a positive integer")

    @staticmethod
    def _require_status(intent, *allowed):
        if intent.status not in allowed:
            raise InvalidState(
                f"{intent.id} is {intent.status}; expected one of {', '.join(allowed)}"
            )

    @staticmethod
    def _intent_payload(intent):
        return {
            "id": intent.id,
            "customer": intent.customer_id,
            "amount": intent.amount,
            "currency": intent.currency,
            "status": intent.status,
        }
