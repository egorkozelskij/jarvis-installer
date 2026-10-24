"""Small dependency graph used by Atlas.

Contract CORE-CLEANUP-ORDER-001: disposing a Computed releases its sources in
reverse order of their first read in the latest run, then runs its cleanup
handlers in reverse registration order. Exceptions from release hooks and
handlers do not stop disposal; they are collected in execution order and
raised together as one ExceptionGroup.
"""


class Source:
    def __init__(self, name, value, on_release=None):
        self.name = name
        self._value = value
        self._subscribers = []
        self._on_release = on_release

    def set(self, value):
        if value == self._value:
            return
        self._value = value
        for consumer in list(self._subscribers):
            consumer._dirty = True

    def _subscribe(self, consumer):
        self._subscribers.append(consumer)

    def _unsubscribe(self, consumer):
        self._subscribers.remove(consumer)
        if self._on_release is not None:
            self._on_release(self, consumer)


class Computed:
    def __init__(self, fn):
        self._fn = fn
        self._deps = []
        self._cleanups = []
        self._dirty = True
        self._value = None
        self._disposed = False

    def on_cleanup(self, handler):
        self._cleanups.append(handler)

    @property
    def value(self):
        if self._disposed:
            raise RuntimeError('disposed')
        if self._dirty:
            self._run()
        return self._value

    def _run(self):
        seen = []

        def read(source):
            if source not in seen:
                seen.append(source)
            return source._value

        self._value = self._fn(read)
        for source in self._deps:
            if source not in seen:
                source._unsubscribe(self)
        for source in seen:
            if source not in self._deps:
                source._subscribe(self)
        self._deps = seen
        self._dirty = False

    def dispose(self):
        if self._disposed:
            return
        self._disposed = True
        errors = []
        for source in reversed(self._deps):
            try:
                source._unsubscribe(self)
            except Exception as exc:  # collected, disposal continues
                errors.append(exc)
        self._deps = []
        for handler in reversed(self._cleanups):
            try:
                handler()
            except Exception as exc:
                errors.append(exc)
        self._cleanups = []
        if errors:
            raise ExceptionGroup('dispose failed', errors)
