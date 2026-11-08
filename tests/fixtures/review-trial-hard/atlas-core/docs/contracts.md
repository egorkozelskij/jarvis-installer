# Behavior guarantees

Consumers of Atlas rely on these guarantees. Changing any of them is a
breaking change and needs an explicit decision.

1. `Computed.value` is recomputed lazily, only after a source it read changed.
2. A source read several times in one run is subscribed once.
3. Sources that were not read in the latest run are released immediately.
4. `dispose()` releases sources in reverse order of their first read in the
   latest run, then runs cleanup handlers in reverse registration order.
   Exceptions from release hooks and handlers do not stop disposal; they are
   collected in execution order and raised together as one ExceptionGroup.
5. Disposing twice is a no-op; reading a disposed value raises RuntimeError.
