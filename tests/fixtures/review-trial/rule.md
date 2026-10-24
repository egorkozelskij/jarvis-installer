### CORE-CLEANUP-ORDER-001 — Disposal follows reverse read order

- Scope: `atlas-core/atlas_core/graph.py`.
- Invariant: disposing a `Computed` releases its sources in reverse order of their first read in the latest run, then runs cleanup handlers in reverse registration order; exceptions are aggregated in execution order.
- Safe path: keep one ordered dependency list as the source of truth for disposal.
- Forbidden: changing the observable release or error order, including for performance.
- Evidence: `contract` — `tests/test_graph.py`; `review` — trace every disposal path.
- Reason: consumers tear down resources in release order.
