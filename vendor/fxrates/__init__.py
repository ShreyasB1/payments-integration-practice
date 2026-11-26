"""fxrates 1.4: fixed reference exchange rates.

Vendored third-party library. Do not edit. See README.md for usage.
"""
from decimal import Decimal

__version__ = "1.4.0"

# How many units of each currency equal 1 USD, in major units.
_PER_USD = {
    "usd": Decimal("1"),
    "eur": Decimal("0.92"),
    "gbp": Decimal("0.80"),
    "jpy": Decimal("150"),
}

# Digits after the decimal point for each currency's minor unit.
MINOR_UNIT_DIGITS = {"usd": 2, "eur": 2, "gbp": 2, "jpy": 0}


class UnsupportedCurrency(ValueError):
    pass


def _check(currency):
    if currency not in _PER_USD:
        raise UnsupportedCurrency(currency)


def rate(from_currency, to_currency):
    """Units of to_currency per 1 unit of from_currency, in MAJOR units."""
    _check(from_currency)
    _check(to_currency)
    return _PER_USD[to_currency] / _PER_USD[from_currency]


def convert(amount_minor, from_currency, to_currency):
    """Convert an amount in minor units. Returns an UNROUNDED Decimal in the
    target currency's minor units. Rounding is the caller's job."""
    _check(from_currency)
    _check(to_currency)
    major = Decimal(amount_minor).scaleb(-MINOR_UNIT_DIGITS[from_currency])
    converted = major * rate(from_currency, to_currency)
    return converted.scaleb(MINOR_UNIT_DIGITS[to_currency])
