# Explore: context map

Explain how the selected part of the project really works. Do not modify files.

1. Read the applicable rules; do not load neighbouring branches by analogy.
2. Establish the actual scope and repository boundaries. Folder names are not
   proof of architecture.
3. Find entrypoints, owners of mutable state, public contracts and the nearest
   consumers.
4. Trace the main read, write and side-effect paths through real calls,
   including creation, reset, disposal and cleanup order.
5. Separate the canonical design from legacy code, unfinished work and your
   own assumptions.
6. If code and rules disagree, show the disagreement; do not silently choose.

Return a short context brief:

- purpose and boundary of the scope;
- entrypoints and source of truth;
- state owners and side effects;
- main data flow and lifecycle;
- public contracts and external dependencies;
- confirmed risks and unknown places;
- links to the key files.

Static reading is not runtime, browser, CI or deployment evidence. Say which
claims come from reading and which from something that was actually executed.
Do not propose a large refactor unless asked.
