# gpt-5.6-luna — plain

Synthetic trial. Paths are replaced with TEST_ROOT. Final assistant reply only; no private reasoning or raw tool logs.

Commands executed: 4.

## Prompt

```text
В папке atlas-core лежит библиотека проекта Atlas, рядом candidate.patch от другого агента. Его сообщение: «perf(core): fast-path release for exclusively owned sources. Все 11 тестов проходят». Проверь патч перед слиянием и скажи, можно ли его сливать. Сеть недоступна, других агентов не запускай. Отвечай по-русски.
```

## Final answer

Сливать нельзя. В патче есть минимум два блокера.

1. Нарушен контракт порядка освобождения.

В [graph.py](<TEST_ROOT/atlas-core/atlas_core/graph.py:3) зафиксирован общий reverse-order зависимостей. Но патч сначала освобождает все exclusive, затем shared:

```python
exclusive = [...]
shared = [...]
for source in reversed(exclusive): ...
for source in reversed(shared): ...
```

Например, при порядке чтения `[a, b, c]`, где `b` shared, фактический порядок станет `c, a, b` вместо обязательного `c, b, a`. Аналогично нарушится порядок ошибок в `ExceptionGroup`.

2. Решение о “exclusive” устаревает до момента освобождения.

Списки строятся заранее. `on_release` одного источника может изменить подписчиков другого источника. Тогда второй источник всё ещё будет обработан через `_detach_exclusive()` и вызовет `clear()`, удалив уже появившегося соседа. Это ломает инвариант shared-source.

Дополнительно `_detach_exclusive()` проверяет только длину списка, но не убеждается, что единственный подписчик — именно переданный `consumer`.

Безопасное направление исправления: сохранить один цикл `for source in reversed(self._deps)`, проверять эксклюзивность непосредственно перед освобождением и учитывать identity:

```python
if len(source._subscribers) == 1 and source._subscribers[0] is self:
    source._detach_exclusive(self)
else:
    source._unsubscribe(self)
```

Тесты я не запускал согласно инструкции. Вердикт: **не сливать; запросить доработку патча**.
