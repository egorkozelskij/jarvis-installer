# Experiment report

The reader must understand the result without opening raw data. Use
`modules/experiments/templates/experiment-report.md`.

Include:

- what approach or algorithm was tested and why;
- the result: improved, not improved, or not established;
- the reason, or an explicit statement that the cause is unknown — a
  hypothesis is not a proven cause;
- versions, environment and scenarios actually run;
- time spent preparing, waiting and running;
- errors, unfinished cells, noise and limits of the conclusion.

Keep a preliminary signal, a confirmed improvement and a comparative ranking
apart. Historical numbers of other projects stay labelled as historical; they
are not a fresh joint measurement.

Keep raw samples, traces and large logs as separate run artifacts and link to
them. Attach only a small data file when it helps verify a specific claim.
Redrawing a chart from saved data is not a new run, and a successful run of a
different revision does not confirm the current patch.
