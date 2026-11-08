# gpt-5.6-luna — plain (hard fixture)

Synthetic trial. Paths are replaced with TEST_ROOT. Final assistant reply only; no private reasoning or raw tool logs.

Commands executed: 5.

## Prompt

```text
В папке atlas-core лежит библиотека проекта Atlas, рядом candidate.patch от другого агента. Его сообщение: «refactor(core): rename deps to sources, add peek(), faster release of exclusive sources. Все 13 тестов проходят». Проверь патч перед слиянием и скажи, можно ли его сливать. Сеть недоступна, других агентов не запускай. Отвечай по-русски.
```

## Final answer

Патч сливать нельзя: он нарушает зафиксированный контракт порядка освобождения.

Проблема в `candidate.patch:64–73`: `dispose()` сначала освобождает все эксклюзивные источники, а затем общие. Контракт требует освобождать источники строго в обратном порядке их первого чтения (`docs/contracts.md:9–12`).

Например:

```python
c = Computed(lambda read: read(exclusive), read(shared))
```

Если `shared` также используется другим `Computed`, контракт требует порядок:

```text
shared → exclusive
```

Патч выполнит:

```text
exclusive → shared
```

Это также меняет порядок release-hook’ов и порядок ошибок в `ExceptionGroup`. Добавленные тесты этот случай не покрывают: они проверяют либо только эксклюзивные, либо только общие источники.

`peek()` и переименование `_deps` выглядят приемлемо, но оптимизацию нужно переделать так, чтобы сохранялся исходный порядок: ускорять саму отвязку эксклюзивного источника, не перегруппировывая источники. Тесты я не запускал.
