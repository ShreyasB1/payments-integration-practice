# Part 4 of 4: Customer balance in any currency

Finance wants each customer's net total in the currency of their choice. Read `vendor/fxrates/README.md` first.

## Requirements

Add `PaymentService.customer_balance(customer_id, currency="usd")`:

- Include only the customer's `succeeded` payments, counting each as `amount - amount_refunded`.
- Convert each payment into the requested currency with `fxrates.convert`.
- Round **once**, on the total, to a whole number of minor units, using banker's rounding (`decimal.ROUND_HALF_EVEN`). Return an `int`.
- Any currency `fxrates` supports is allowed, including `jpy`, even though payments can't be created in it.
- An unsupported currency raises `InvalidRequest`, not the library's own error.
- An unknown customer raises `NotFound`.

## Example

```python
cus = svc.create_customer("ana@example.com")
usd = svc.create_payment_intent(cus.id, 1000)          # $10.00
eur = svc.create_payment_intent(cus.id, 920, "eur")    # €9.20
svc.confirm(usd.id); svc.confirm(eur.id)

svc.customer_balance(cus.id)          # 2000   ($20.00)
svc.customer_balance(cus.id, "jpy")   # 3000   (¥3,000)
svc.customer_balance(cus.id, "cad")   # raises InvalidRequest
```

## Tests you must write

Write these in `tests/test_part4.py`. Work out each expected number by hand first, using the examples in the fxrates README.

- Payments in USD and EUR, reported in USD, EUR and JPY.
- Only succeeded payments count, and refunds are subtracted. Include a payment that was never confirmed and one that was canceled.
- Rounding happens once on the total. Find three small payments where rounding each one first gives a different answer from rounding the total.
- Banker's rounding: an exact half rounds to the even number.
- A customer with no payments has a balance of 0, and the result is an `int`.
- An unsupported currency raises `InvalidRequest`, even for a customer with no payments, and an unknown customer raises `NotFound`.

```bash
python3 -m pytest
```
