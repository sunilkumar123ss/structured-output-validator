# Strict structured-output validator

> **Disclosed reconstruction prepared on 24 October 2026.** The recorded Git dates are synthetic, not dates of past development. See [HISTORY.md](HISTORY.md).

This is an incomplete stage in a tutorial reconstruction of an already-completed reference implementation. Source, fixtures, tests, command-line behavior and verification are introduced in later stages. Only the final branch tip contains the complete documented package.

## Intended scope of the final example

Validates a small documented JSON Schema-inspired subset: type, properties, required, additionalProperties, items, enum, string length, number bounds, and array length. Unsupported schema keywords fail explicitly. JSON parsing rejects NaN/Infinity and duplicate keys. Booleans are not accepted as numbers. This is not a complete JSON Schema implementation and cannot verify the factual truth of valid-shaped outputs.

All examples are synthetic and educational. This reconstruction does not establish historical employment, deployment, usage, or production benchmarks.
