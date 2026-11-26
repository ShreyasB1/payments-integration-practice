"""Existing tests. These must keep passing after every change you make."""
import pytest

from payments.errors import InvalidRequest, InvalidState, NotFound
from payments.service import PaymentService


@pytest.fixture
def svc():
    return PaymentService()


@pytest.fixture
def customer(svc):
    return svc.create_customer("ana@example.com")


def test_create_customer_assigns_ids(svc):
    assert svc.create_customer("a@x.com").id == "cus_1"
    assert svc.create_customer("b@x.com").id == "cus_2"


def test_create_customer_rejects_bad_email(svc):
    with pytest.raises(InvalidRequest):
        svc.create_customer("not-an-email")


def test_create_and_confirm(svc, customer):
    intent = svc.create_payment_intent(customer.id, 5000)
    assert (intent.id, intent.status, intent.currency) == ("pi_1", "requires_confirmation", "usd")
    assert svc.confirm(intent.id).status == "succeeded"


def test_currency_is_lowercased(svc, customer):
    assert svc.create_payment_intent(customer.id, 100, "EUR").currency == "eur"


@pytest.mark.parametrize("amount", [0, -5, 10.5, "100", True])
def test_rejects_bad_amounts(svc, customer, amount):
    with pytest.raises(InvalidRequest):
        svc.create_payment_intent(customer.id, amount)


def test_rejects_unknown_customer_and_currency(svc, customer):
    with pytest.raises(NotFound):
        svc.create_payment_intent("cus_404", 100)
    with pytest.raises(InvalidRequest):
        svc.create_payment_intent(customer.id, 100, "cad")


def test_cannot_confirm_twice_or_after_cancel(svc, customer):
    first = svc.create_payment_intent(customer.id, 100)
    svc.confirm(first.id)
    with pytest.raises(InvalidState):
        svc.confirm(first.id)
    second = svc.create_payment_intent(customer.id, 100)
    svc.cancel(second.id)
    with pytest.raises(InvalidState):
        svc.confirm(second.id)


def test_list_payments_filters_by_customer_and_status(svc, customer):
    other = svc.create_customer("bo@example.com")
    a = svc.create_payment_intent(customer.id, 100)
    b = svc.create_payment_intent(customer.id, 200)
    svc.create_payment_intent(other.id, 300)
    svc.confirm(a.id)
    assert svc.list_payments(customer.id) == [a, b]
    assert svc.list_payments(customer.id, status="succeeded") == [a]


def test_event_payloads_are_stable(svc, customer):
    """Other teams depend on these payloads. Don't change their shape."""
    intent = svc.create_payment_intent(customer.id, 700, "gbp")
    svc.confirm(intent.id)
    assert [e.type for e in svc.bus.history] == [
        "customer.created", "payment_intent.created", "payment_intent.succeeded"]
    assert svc.bus.history[-1].data == {
        "id": "pi_1", "customer": "cus_1", "amount": 700,
        "currency": "gbp", "status": "succeeded"}
