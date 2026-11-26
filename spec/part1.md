# Part 1 of 4: Refunds

Customers sometimes need their money back. Add refunds to the service.

## Requirements

1. Add an `amount_refunded` field to `PaymentIntent`, starting at 0.
2. Add a `Refund` model with these fields: `id`, `payment_intent_id`, `amount` (minor units) and `reason` (a string or `None`).
3. Add `PaymentService.refund(intent_id, amount=None, reason=None)`:
   - Only a `succeeded` payment can be refunded. Otherwise raise `InvalidState`.
   - With no amount, refund everything that's left.
   - The amount must be a positive integer no larger than what's left. Otherwise raise `InvalidRequest`.
   - Store the refund with ids `re_1`, `re_2`, and so on, and add the amount to `amount_refunded`.
   - Publish a `charge.refunded` event with the data `{"refund": <refund id>, "payment_intent": <intent id>, "amount": <amount>}`.
   - Return the `Refund`.
4. Add `PaymentService.list_refunds(intent_id)`, which returns that payment's refunds in the order they were made.

A payment's `status` stays `succeeded`, even when fully refunded.

## Example

```python
svc = PaymentService()
cus = svc.create_customer("ana@example.com")
pi = svc.create_payment_intent(cus.id, 5000)
svc.confirm(pi.id)

svc.refund(pi.id, 2000)                 # Refund(id="re_1", payment_intent_id="pi_1", amount=2000, reason=None)
svc.refund(pi.id, reason="duplicate")   # refunds the remaining 3000 as re_2
pi.amount_refunded                      # 5000
svc.refund(pi.id, 1)                    # raises InvalidRequest
```

## Tests you must write

Write these in `tests/test_part1.py`. Each bullet should be at least one test.

- A partial refund, then a refund with no amount that takes the rest. Check the ids, amounts and `amount_refunded`.
- A new payment starts with `amount_refunded` of 0.
- Bad amounts are rejected: zero, negative, more than what's left, a float, and `True`. Check that a rejected refund changes nothing, including the event history.
- A refund after the payment is fully refunded is rejected.
- Refunding a payment that hasn't succeeded raises `InvalidState`, and an unknown id raises `NotFound`.
- The `charge.refunded` event has exactly the data in the spec.
- `list_refunds` returns refunds in order, and only for that payment.

When they pass, run every test so you know nothing older broke:

```bash
python3 -m pytest
```
