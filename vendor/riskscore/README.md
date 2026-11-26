# riskscore 2.1

Scores a card transaction for fraud risk.

## Usage

```python
import riskscore

assessment = riskscore.evaluate(riskscore.Transaction(
    amount=600_000,          # minor units
    currency="usd",
    customer_id="cus_1",
    email="ana@example.com",
    prior_payments=0,
))
assessment.score      # 70
assessment.decision   # "review"
assessment.reasons    # ("large_amount", "new_customer")
```

## API

`evaluate(txn, *, review_threshold=60, block_threshold=85) -> Assessment`

- `txn` must be a `riskscore.Transaction`. Any other type raises `RiskscoreError`.
- Raises `RiskscoreError` for a non-positive amount or an unsupported currency.
- Supported currencies: `usd`, `eur`, `gbp`.

`Transaction` fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `amount` | int | Amount in minor units |
| `currency` | str | Lowercase ISO code |
| `customer_id` | str | Your customer's ID |
| `email` | str | Your customer's email |
| `prior_payments` | int | How many successful payments the customer made before this one. Defaults to 0. |

`Assessment` fields: `score` (0 to 100), `decision` (one of `riskscore.ALLOW`, `riskscore.REVIEW`, `riskscore.BLOCK`) and `reasons` (a tuple of strings).

## Scoring

| Signal | Points |
| --- | --- |
| Amount of at least $5,000 | +50 |
| Amount of at least $1,000 (and under $5,000) | +25 |
| `prior_payments` is 0 | +20 |
| Email on a disposable domain | +30 |

A score at or above `block_threshold` is `block`. At or above `review_threshold` is `review`. Anything lower is `allow`.
