"""Hidden acceptance scenario: not shown to agents."""
import sys
sys.path.insert(0, sys.argv[1])
from atlas_core.graph import Computed, Source

log = []
def boom(s, c):
    log.append(s.name)
    raise ValueError(s.name)
sources = [Source(str(i), i, boom) for i in range(64)]
def fn(read):
    total = sum(read(s) for s in sources)
    total += sum(read(s) for s in reversed(sources))
    return total + read(sources[1])
target = Computed(fn)
neighbour = Computed(lambda read: sum(read(s) for s in sources[::2]))
target.value, neighbour.value
try:
    target.dispose()
except ExceptionGroup as g:
    errs = [str(e) for e in g.exceptions]
expected = [str(i) for i in range(63, -1, -1)]
print('value', fn(lambda s: s._value), 'release ok', log == expected, 'errors ok', errs == expected, 'tail', log[-3:])
