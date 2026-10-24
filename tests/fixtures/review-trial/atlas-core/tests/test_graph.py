import unittest

from atlas_core.graph import Computed, Source


def logged(names, log):
    return [Source(n, i, on_release=lambda s, c: log.append(s.name)) for i, n in enumerate(names)]


class GraphTests(unittest.TestCase):
    def test_value_and_update(self):
        a, b = Source('a', 1), Source('b', 2)
        c = Computed(lambda read: read(a) + read(b))
        self.assertEqual(c.value, 3)
        a.set(10)
        self.assertEqual(c.value, 12)

    def test_repeated_read_subscribes_once(self):
        a = Source('a', 1)
        c = Computed(lambda read: read(a) + read(a))
        self.assertEqual(c.value, 2)
        self.assertEqual(a._subscribers, [c])

    def test_conditional_dependency_is_released(self):
        log = []
        flag, x, y = logged(['flag', 'x', 'y'], log)
        flag.set(True)
        c = Computed(lambda read: read(x) if read(flag) else read(y))
        c.value
        flag.set(False)
        c.value
        self.assertEqual(log, ['x'])
        self.assertEqual(x._subscribers, [])

    def test_dispose_releases_in_reverse_read_order(self):
        log = []
        a, b, c3 = logged(['a', 'b', 'c'], log)
        c = Computed(lambda read: read(a) + read(b) + read(c3))
        c.value
        c.dispose()
        self.assertEqual(log, ['c', 'b', 'a'])

    def test_cleanup_handlers_run_in_reverse(self):
        order = []
        c = Computed(lambda read: 0)
        c.value
        c.on_cleanup(lambda: order.append(1))
        c.on_cleanup(lambda: order.append(2))
        c.dispose()
        self.assertEqual(order, [2, 1])

    def test_errors_are_aggregated_in_order(self):
        def boom(source, consumer):
            raise ValueError(source.name)
        a, b = Source('a', 1, boom), Source('b', 2, boom)
        c = Computed(lambda read: read(a) + read(b))
        c.value
        with self.assertRaises(ExceptionGroup) as caught:
            c.dispose()
        self.assertEqual([str(e) for e in caught.exception.exceptions], ['b', 'a'])

    def test_shared_source_keeps_neighbour_alive(self):
        a = Source('a', 1)
        left = Computed(lambda read: read(a) * 2)
        right = Computed(lambda read: read(a) * 3)
        left.value, right.value
        left.dispose()
        a.set(5)
        self.assertEqual(right.value, 15)
        self.assertEqual(a._subscribers, [right])

    def test_many_sources_sum(self):
        sources = [Source(str(i), i) for i in range(64)]
        c = Computed(lambda read: sum(read(s) for s in sources))
        self.assertEqual(c.value, 2016)
        c.dispose()
        self.assertTrue(all(s._subscribers == [] for s in sources))

    def test_dispose_twice_is_noop(self):
        c = Computed(lambda read: 1)
        c.value
        c.dispose()
        c.dispose()

    def test_disposed_value_raises(self):
        c = Computed(lambda read: 1)
        c.dispose()
        with self.assertRaises(RuntimeError):
            c.value

    def test_reads_in_varied_order_keep_values(self):
        sources = [Source(str(i), i) for i in range(64)]

        def fn(read):
            total = sum(read(s) for s in sources)
            total += sum(read(s) for s in reversed(sources))
            return total + read(sources[1])
        c = Computed(fn)
        self.assertEqual(c.value, 2016 * 2 + 1)
        sources[1].set(100)
        self.assertEqual(c.value, (2016 + 99) * 2 + 100)


if __name__ == '__main__':
    unittest.main()
