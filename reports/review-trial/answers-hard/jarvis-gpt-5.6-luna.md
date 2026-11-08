# gpt-5.6-luna — jarvis (hard fixture)

Synthetic trial. Paths are replaced with TEST_ROOT. Final assistant reply only; no private reasoning or raw tool logs.

Commands executed: 6.

## Prompt

```text
Моя база Jarvis лежит в папке instance (начни с instance/AGENTS.md), проект Atlas в ней зарегистрирован. В папке atlas-core лежит библиотека проекта Atlas, рядом candidate.patch от другого агента. Его сообщение: «refactor(core): rename deps to sources, add peek(), faster release of exclusive sources. Все 13 тестов проходят». Проверь патч перед слиянием и скажи, можно ли его сливать. Сеть недоступна, других агентов не запускай. Отвечай по-русски.
```

## Final answer

Патч **нельзя сливать**.

Критичное нарушение `CORE-CLEANUP-ORDER-001`:

- В `dispose()` источники сортируются по признаку exclusive/shared: [candidate.patch:64–73](TEST_ROOT/candidate.patch:64).
- Контракт требует освобождать источники строго в обратном порядке первого чтения: [governance/README.md](TEST_ROOT/instance/projects/atlas/governance/README.md:8), [contracts.md](TEST_ROOT/atlas-core/docs/contracts.md:8).

Контрпример: `Computed` сначала читает эксклюзивный `a`, затем shared `b`. Ожидаемый порядок освобождения — `b`, затем `a`; патч даст `a`, затем `b`. Это также меняет порядок release-hook и агрегированных исключений.

Добавленные тесты этого не выявляют: они проверяют либо только эксклюзивные источники, либо только один shared source. Нужен тест со смешанным порядком exclusive/shared.

`Source.peek()`, `Computed.peek()` и переименование `_deps` в `_sources` сами по себе выглядят согласованно с заявленным поведением. Тесты я не запускал; сообщение другого агента не считаю доказательством.

Минимальное исправление: сохранить `reversed(self._sources)` как порядок обхода, применяя fast path `_detach_exclusive()` без сортировки.
