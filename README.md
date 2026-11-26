# Payments Integration Practice

A practice codebase for the Integration round of a software engineering interview. You extend existing code, use two third-party libraries from their docs, keep the existing tests passing, and write your own tests for everything you add. This is an original practice exercise, not Stripe material.

## Setup (do this before you start the timer)

You need Python 3.10 or newer.

```bash
pip install pytest
python3 -m pytest        # the 13 existing tests should pass
```

Run everything from the repo's top folder. `conftest.py` makes `payments` and the libraries in `vendor/` importable, so `import riskscore` and `import fxrates` work in your code.

## What's here

| Path | What it is | Can you edit it? |
| --- | --- | --- |
| `payments/` | The service you'll extend | Yes |
| `tests/test_service.py` | Existing tests | Don't change these; they must keep passing |
| `tests/test_part1.py` to `test_part4.py` | Empty files for your own tests | Yes, this is where your tests go |
| `vendor/riskscore/` | Fraud-scoring library, with a README | No |
| `vendor/fxrates/` | Exchange-rate library, with a README | No |
| `spec/part1.md` to `part4.md` | The tasks, one per file | Read only |

## How to run a mock round (60 minutes)

1. **Minutes 0 to 5:** Create a branch (below). Open `spec/part1.md` only, skim `payments/service.py`, and run the existing tests.
2. **Minutes 5 to 55:** Work through the parts in order. For each part:
   1. Read the spec, and any library docs it points to.
   2. Write the code.
   3. Write the tests listed under "Tests you must write" in that part's spec.
   4. Run `python3 -m pytest`, so the old tests and your new ones all run.
   5. Commit, then open the next spec file.
3. **Talk out loud the whole time,** as if an interviewer were watching.

Most people won't finish all four parts in an hour. Parts 1 and 2 done cleanly, with good tests, is a solid result.

## Writing good tests

- **Test behavior, not code.** Call the service the way a user would and check what comes back.
- **One idea per test,** with a name that says what it proves, such as `test_rejected_refund_changes_nothing`.
- **Cover the edges:** zero, negative, too large, exactly at the limit, empty, and unknown ids.
- **Check failures change nothing.** After a rejected request, confirm the state and the event history are untouched.
- **Work out expected values by hand** from the spec or docs before running the test, so the test can actually catch a bug.
- **Use `pytest.raises`** for errors and `pytest.mark.parametrize` for the same check across several inputs.

## Using git for practice

```bash
git checkout -b attempt-1        # do each attempt on its own branch
git add -A && git commit -m "Part 1: refunds"
```

To start fresh, go back to `main` and make a new branch: `git checkout main && git checkout -b attempt-2`. The `main` branch always holds the untouched starter code.

## Checking your work afterwards

The separate solution download has a `checks/` folder of acceptance tests. Once you've finished, copy it into this repo and run `python3 -m pytest checks` to see whether your code meets the spec. Compare its tests with yours to find cases you missed. Keep `checks/` off your branch until then.

## Rules

- **Extend, don't rewrite.** Keep the existing structure and style.
- **Read the library READMEs before using them.** Each has at least one detail that's easy to get wrong.
- **No AI tools.** Docs and Stack Overflow are fine, as in the real round.
