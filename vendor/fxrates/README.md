# fxrates 1.4

Fixed reference exchange rates for reporting.

## Supported currencies

`usd`, `eur`, `gbp`, `jpy`. Anything else raises `fxrates.UnsupportedCurrency`, a subclass of `ValueError`.

## API

`rate(from_currency, to_currency) -> Decimal`

How many units of `to_currency` equal one unit of `from_currency`, in **major** units (dollars, not cents).

```python
fxrates.rate("usd", "eur")   # Decimal('0.92')
```

`convert(amount_minor, from_currency, to_currency) -> Decimal`

Converts an amount given in **minor** units and returns the result in the target currency's minor units. It accounts for currencies with different minor units: JPY has none, so 100 USD cents becomes 150 yen.

The result is **not rounded**. Round it yourself, once, at the point where you need a whole number.

```python
fxrates.convert(1000, "usd", "eur")   # Decimal('920.00')   ($10.00 -> €9.20)
fxrates.convert(100, "usd", "jpy")    # Decimal('150')      ($1.00 -> ¥150)
fxrates.convert(1, "gbp", "usd")      # Decimal('1.25')     (unrounded)
```

`MINOR_UNIT_DIGITS` maps each currency to its number of minor-unit digits, e.g. `{"usd": 2, "jpy": 0}`.
