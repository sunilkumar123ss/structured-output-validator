# Strict structured-output validator

Runnable educational demo/starter with synthetic examples.

Validates a small documented JSON Schema-inspired subset: type, properties, required, additionalProperties, items, enum, string length, number bounds, and array length. Unsupported schema keywords fail explicitly. JSON parsing rejects NaN/Infinity and duplicate keys. Booleans are not accepted as numbers. This is not a complete JSON Schema implementation and cannot verify the factual truth of valid-shaped outputs.

## Run

Python 3.10+; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

No network requests, credentials, or paid services are used. Any model/provider integration would be a separate adapter. Read `main.py` for the public functions and `test_main.py` for success/failure invariants. Fixture content is synthetic.

## Scope

This is an educational implementation with synthetic fixtures. Run the tests and inspect the documented limits before adapting it.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
