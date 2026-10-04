# Work from the app, not from a questionnaire

Use this operating guide with any Mobile App Builder command or lead agent. Its purpose is to get to the first useful result quickly while preserving project context. It does not authorize network calls, paid research, account changes or publication.

## First move

1. Restate the user's desired result in plain language and identify whether this is an idea, an existing app or one focused task.
2. For an existing repository, read its instructions and inspect only the relevant code, manifests, recent changes and available evidence. The optional local helper can provide a small manifest snapshot:

   ```text
   node scripts/inspect-project.mjs /path/to/app --goal "the user's outcome"
   ```

   The helper reads only selected public project manifests, never environment files, source contents, analytics accounts or credentials. Its output is a starting clue, not proof that a platform builds or a feature works. For an idea without a repository, skip it.
3. Choose the smallest relevant entry skill and detailed guide. Add another lead only when a handoff is needed. The eight commands are shortcuts, not a fixed process everyone must follow.
4. Take authorized, reversible steps that move the request forward. Ask one concise question only when a missing answer changes the next dependent action.

## Carry context across sessions

Use the project's existing issue, brief or planning file where one exists. Otherwise, after the first substantive task, offer a concise user-owned Markdown context card in the consuming project using [the context template](../templates/project-context.md). Keep it reviewable and easy to delete. Suggested fields:

| Field | Record |
| --- | --- |
| Product | Audience, user problem and first useful result |
| Reality | Actual stack, target platforms, routes and data boundaries |
| Direction | Accepted design, architecture and product decisions, with date and source |
| Evidence | Observed result, source, sample, recency and confidence |
| Current task | Outcome, constraints, acceptance and authorized scope |
| Verification | Source commit, tests, build, device, deployed URL and store state separately |
| Next action | One recommended move, why it matters and what would change it |

Read this card and current repository evidence on later tasks. Never treat a stale card as current device, analytics, store or build proof. Update only decision-relevant facts. Keep transcripts, tokens, raw customer records, private datasets and undisclosed telemetry out of it. Do not silently publish the card.

## Make a useful recommendation

When several actions are possible, rank them by user impact, supporting evidence, cost/effort and reversal risk. Say which observation supports the top action and what remains uncertain. For “onboarding feels weak,” inspect the real journey and available activation evidence first; then choose design, implementation and QA work that addresses the observed friction. For “I have a new app idea,” validate the problem and first useful journey before selecting infrastructure.

Use confidence labels rather than invented precise probabilities. An instinctive next step is a well-supported inference that can be revised when new evidence appears.

## Report the result at the right depth

A focused fix needs a short result, changed behavior, affected checks and remaining limitation. A multi-finding audit, comparison, launch review or ongoing watch benefits from a visual report. Prepare a small structured JSON file from real evidence; [the report example](../templates/decision-report.json) shows the accepted shape. Then run:

```text
node scripts/render-report.mjs /path/to/report.json --output /path/to/report.html
```

The renderer creates a self-contained, script-free local HTML file and refuses to overwrite an existing file. It does not upload, track or fetch anything. Check the input for personal data and share only an authorized copy. The report shows signals, findings, next actions and limits; it never substitutes a visual score for missing verification. Open the result for the user when the host supports it.

## Learn without hidden collection

At completion, make correction easy: point to the result and invite the user to name a wrong route, stale assumption, incomplete step or failed check. Do not insert a survey into every task. For feedback the user wants to share with the plugin publisher, use the [optional feedback route](FEEDBACK.md). Keep user-project feedback in that project unless the user explicitly submits it.

When a task is repeatable and the user requests ongoing help, use the [recurring-work recipes](RECURRING-WORK.md). Schedules belong to the user's host account; a plugin installation does not create one.
