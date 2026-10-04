# Scheduled work that earns its next run

Mobile App Builder does not create a schedule on installation. A user may choose a recurring outcome after seeing a useful one-time result. Claude Code Routines can run on a schedule, as can local Desktop scheduled tasks; availability, account usage and capabilities depend on the host. Cloud routines may execute autonomously with access to selected repositories and connectors. Scope those inputs to the task. See the current [Claude Code Routines documentation](https://code.claude.com/docs/en/routines) and [local scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks).

For every schedule, confirm the project, cadence and timezone, sources, allowed tools, cost boundary, output location, alert threshold and pause/delete path. Start with a read-only or draft-only run. If the host lacks scheduling, provide a reusable prompt instead of pretending a task was created. A completed run is not proof that the requested check succeeded; inspect its actual output.

## Weekly app health review

```text
Each week, inspect this app's current repository and the first-party error or analytics sources I have explicitly connected. Compare with the last verified report. Report only changed critical journeys, new high-impact errors and release risks. Cite exact source/build/time. Recommend one reversible next action. If nothing meaningful changed, give a one-line unchanged result. Do not deploy, spend, contact anyone or publish.
```

## Store and competitor changes

```text
Each week, review the named Apple App Store and Google Play competitors using public or already authorized sources. Compare listing copy, screenshots, ratings and bounded review themes with the last saved evidence. Show only meaningful changes, source dates and uncertainties. Propose one original experiment. Do not launch collection with a new cost, contact creators, change listings or publish.
```

## SEO and discovery review

```text
Each month, compare the app website's technical crawl, search performance and content priorities against the previous verified report, using only sources I have connected. Separate web SEO from app-store optimization. Flag regressions and one priority improvement, with evidence and a check plan. Do not edit production or buy ads.
```

## Pre-release check

```text
Before the planned release window, inspect the exact commit, CI run, target build, known-device results, store assets and unresolved privacy/review items. Return pass, fail or unknown for each gate with its evidence. Prepare a draft fix or checklist for review; do not upload or submit the app.
```

After a first run, review whether the report was actionable and whether it caused unnecessary noise. Pause or narrow a recipe that does not produce useful change. Session count is not the success measure; confirmed decisions, fixes, avoided regressions and user time saved are.
