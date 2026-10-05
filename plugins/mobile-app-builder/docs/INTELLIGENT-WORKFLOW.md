# Work from the app, not from a questionnaire

Use this operating guide with any Mobile App Builder command or lead agent. Its purpose is to get to the first useful result quickly while preserving project context. It does not authorize network calls, paid research, account changes or publication.

## First move

1. Restate the user's desired result in plain language and identify whether this is an idea, an existing app or one focused task.
2. For an existing repository, read its instructions and inspect only the relevant code, manifests, recent changes and available evidence. The optional local helper can provide a small manifest snapshot:

   ```text
   node scripts/inspect-project.mjs /path/to/app --goal "Fix the login error" --intent fix --task-id login-repair
   ```

   The helper reads only selected public project manifests, never environment files, source contents, analytics accounts or credentials. Its output is a starting clue, not proof that a platform builds or a feature works. For an idea without a repository, skip it.
3. Choose the smallest relevant entry skill and detailed guide. Add another lead only when a handoff is needed. The eight commands are shortcuts, not a fixed process everyone must follow.
4. Take authorized, reversible steps that move the request forward. Ask one concise question only when a missing answer changes the next dependent action.

## Take the shortest route

These routes share the same public skills and command shortcuts. They do not add new mandatory stages. Use the actual request over the inspector's keyword hint. A focused fix does not need market research, onboarding questions or a new architecture proposal.

| Request | First useful result | Relevant entry |
| --- | --- | --- |
| Build a feature | One working slice with affected checks; choose auth, storage, native or UI guidance by the feature | `build-app` |
| Fix a crash or regression | Reproduction, focused repair and the check that would catch it again | `guide-reliability`, `improve-app` |
| Audit the app | Prioritized findings supported by current files or observed behavior; implement fixes within the requested scope | `test-app` |
| Improve a journey | One observed friction removed and verified in the existing design | `improve-app` |
| Import a design or artifact | A mapped, reviewable adaptation that preserves working app behavior | `guide-design-handoff`, `guide-workflow-coordination` |
| Review a change | Actionable findings and affected evidence without unrelated edits | `guide-workflow-coordination` |
| Release a candidate | Exact build/commit, verification gaps and authorized target action | `launch-app` |
| Continue | The next unresolved checkpoint reconciled with current files | `guide-workflow-coordination` |
| Research an idea | One product decision supported by public evidence or a supplied export | `research-app` |

For Chrome extensions, Shopify apps or text processing, use the corresponding product workflow rather than creating a mobile app. Follow explicit user skill selection; do not override it because a keyword matches another route.

## Use an execution receipt

The inspector requires an available Node.js runtime; check its version in the host before use. Do not silently install a global runtime. If it is unavailable, inspect the selected public markers manually and label that evidence. The inspector executes no project code, contacts no service and creates no persistent state. Its [execution contract](EXECUTION-CONTRACT.md) describes input limits, identity, safe errors and recovery. Preserve the receipt's task ID with the existing checkpoint when continuity is useful.

Choose one acceptance condition before editing: for example, the failed login displays a retryable error without blocking the app. Inspect available test scripts before executing them; a manifest's script name is not proof of a safe or installed executable. Apply the app's own toolchain and current platform documentation. For an Android-only defect in a Flutter app, start with the failing Flutter/Android path; do not migrate to Expo or test unrelated store flows.

After a potentially external timeout, mark the outcome **unknown** and read back the same build, submission or research run ID before retrying. Bound status checks to three attempts per task, spaced according to provider guidance, then keep a continuation point. Limit paid research by both records and an approved financial ceiling using the research component; a record limit alone is not a cost limit. Preserve partial results and their source IDs, timestamps, missing fields and conflicts. Never describe replay as safe without provider support.

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

For “continue,” use the task ID, last accepted checkpoint, completed artifacts, unresolved blocker and next action. Reconcile the recorded commit and files first. Preserve valid authorization for the same scope; request a new decision only when the account, cost, target or consequential action has changed. If no checkpoint exists, reconstruct the task from available context before asking the user to repeat it.

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
