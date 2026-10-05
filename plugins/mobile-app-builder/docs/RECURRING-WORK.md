# Scheduled work that earns its next run

Mobile App Builder does not create a schedule on installation. A user may choose a recurring outcome after seeing a useful one-time result. Claude Code Routines can run on a schedule, as can local Desktop scheduled tasks; availability, account usage and capabilities depend on the host. Cloud routines may execute autonomously with access to selected repositories and connectors. Scope those inputs to the task. See the current [Claude Code Routines documentation](https://code.claude.com/docs/en/routines) and [local scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks).

For every schedule, confirm the project, cadence and timezone, sources, allowed tools, cost boundary, output location, alert threshold and pause/delete path. Start with a read-only or draft-only run. If the host lacks scheduling, provide a reusable prompt instead of pretending a task was created. A completed run is not proof that the requested check succeeded; inspect its actual output.

Use the scheduling capability exposed by the current host. In Codex Desktop, use its automation tool for a user-requested follow-up or recurring task, and read back its active status and saved scope. In a host without an available scheduling tool, including a Cursor session where none is exposed, leave the recipe as a reusable prompt and name the missing capability. Do not install a separate scheduler to fill that gap. These recipes work across hosts; their activation depends on the host's supported scheduling feature.

Record the schedule identifier, timezone, next run when supplied, permitted inputs, pause/delete controls and activation readback in the user's existing project context. Keep secrets and private connector data out of it. An activation readback verifies the schedule exists; only a subsequent run with checked output verifies the recurring outcome. Notify the user for a meaningful change, failure or decision rather than every unchanged run, unless they request regular status updates.

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
