"""Your tests for this part. See the "Tests you must write" section of its spec file."""
import pytest

from payments.errors import InvalidRequest, InvalidState, NotFound
from payments.service import PaymentService


@pytest.fixture
def svc():
    return PaymentService()


@pytest.fixture
def customer(svc):
    return svc.create_customer("ana@example.com")


# Write your tests below.
