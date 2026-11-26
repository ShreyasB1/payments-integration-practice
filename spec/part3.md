# Part 3 of 4: Fraud screening with riskscore

Before a payment succeeds, screen it with the vendored `riskscore` library. Read `vendor/riskscore/README.md` first.

## Requirements

In `confirm`, before marking the payment `succeeded`, call `riskscore.evaluate` with:

- the payment's amount and currency,
- the customer's id and email,
- `prior_payments`: how many of this customer's payments have already `succeeded`.

Then act on the decision:

| Decision | New status | Event | What `confirm` does |
| --- | --- | --- | --- |
| allow | `succeeded` | `payment_intent.succeeded` (unchanged) | Returns the intent |
| review | `requires_review` | `payment_intent.requires_review` | Returns the intent |
| block | `blocked` | `payment_intent.blocked` | Raises `PaymentBlocked` |

Also:

- Save the score on the intent as `intent.metadata["risk_score"]`, as a string, in all three cases.
- Add a `PaymentBlocked` error to `payments/errors.py`, as a subclass of `PaymentsError`. Give it a `reasons` attribute holding the assessment's reasons.
- The two new events use the same payload shape as the other payment events.
- Add `approve(intent_id)`, which moves a `requires_review` payment to `succeeded` and publishes `payment_intent.succeeded`. Calling it on any other status raises `InvalidState`.

The existing tests must still pass. Check what risk score they get before you assume they will.

## Example

```python
cus = svc.create_customer("ana@example.com")
pi = svc.create_payment_intent(cus.id, 600_000)    # $6,000, new customer
svc.confirm(pi.id).status                           # "requires_review"
pi.metadata["risk_score"]                           # "70"
svc.approve(pi.id).status                           # "succeeded"
```

## Tests you must write

Write these in `tests/test_part3.py`. Work out each expected score from the scoring table in the library's README before you run the test.

- A small payment from a new customer is allowed, and its `risk_score` is saved.
- A large payment from a new customer goes to review, and the `payment_intent.requires_review` event has the right payload.
- `prior_payments` counts only succeeded payments: a canceled payment doesn't count, but an earlier successful one does.
- A large payment from a disposable email domain is blocked: `confirm` raises `PaymentBlocked` with the right reasons, and the status and event are set.
- A EUR payment is scored in its own currency.
- `approve` moves a payment from review to succeeded, and raises `InvalidState` for any other status.

```bash
python3 -m pytest
```
