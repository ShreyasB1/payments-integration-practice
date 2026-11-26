# Part 2 of 4: Idempotency keys

If a client's network drops after it sends a request, it can't tell whether the payment was created. It needs to retry safely without charging the customer twice.

## Requirements

Add an optional `idempotency_key=None` parameter to `create_payment_intent`.

- **First request with a key:** create the payment as normal, and remember the key.
- **Same key again, same parameters:** return the **same** `PaymentIntent` object. Don't create a new one, don't use up an id, and don't publish another event.
- **Same key again, different parameters:** raise `InvalidRequest`. Compare the customer, amount, currency (after lowercasing) and metadata.
- **A request that fails validation** doesn't use up its key. A corrected retry with the same key should succeed.
- **No key:** behave exactly as before.

## Example

```python
a = svc.create_payment_intent(cus.id, 1000, idempotency_key="order-42")
b = svc.create_payment_intent(cus.id, 1000, idempotency_key="order-42")
a is b                    # True, and only one payment_intent.created event

svc.create_payment_intent(cus.id, 999, idempotency_key="order-42")   # raises InvalidRequest
```

## Tests you must write

Write these in `tests/test_part2.py`.

- The same key with the same parameters returns the same object (check with `is`), publishes only one `payment_intent.created` event, and doesn't use up an id.
- `"USD"` and `"usd"` count as the same currency for the same key.
- Changing each of the amount, currency, metadata and customer with the same key raises `InvalidRequest`. Consider `pytest.mark.parametrize`.
- A request that fails validation doesn't use up its key: the corrected retry with that key succeeds.
- Different keys create different payments.
- Leaving out the key behaves exactly as before.

```bash
python3 -m pytest
```
