# Machine queue — planned

Not installed as a working capability. Several agents that measure, build or
run browsers on one computer disturb each other's timing; separate worktrees
do not separate CPU, memory or disk. The planned module gives agents a shared
queue to quiet machines used for confirming measurements.

Design requirements:

- A request names a concrete owner (agent session), task, source revisions,
  expected duration and a hard time limit.
- One job per machine slot. The slot covers preparation, run, result
  collection and cleanup; installing dependencies also disturbs measurements.
- Ordinary requests are first-in, first-out; priority only by owner decision.
- Running jobs send a heartbeat. An expired estimate is not proof that a
  process may be killed: first establish its real state and its owner.
- Recovery is addressed by owner identity, not by process or folder name. A
  dropped connection does not mark the machine free.
- An optional coordinator periodically checks machines and requests and asks
  the specific owner to act. It does not run tests itself.
- On a workstation coordination stays soft (shared state and agreement); on a
  dedicated machine the tool enforces exclusive access.
- Proving that the queue works is separate from proving that a machine is
  suitable for a given measurement protocol.

No queue tool, server access or coordinator is deployed in this release.
