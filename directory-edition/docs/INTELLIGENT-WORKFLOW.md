# Work from the app, not from a questionnaire

Use this operating guide with any Mobile App Builder command or lead agent. Its purpose is to get to the first useful result quickly while preserving project context. It does not authorize network calls, paid research, account changes or publication.

## First move

1. Restate the user's desired result in plain language and identify whether this is an idea, an existing app or one focused task.
2. For an existing repository, read its instructions and inspect only the relevant code, manifests, recent changes and available evidence. Start with the [manual inspection checklist](EXECUTION-CONTRACT.md): read `package.json` and `app.json` if present, check which framework and platform markers exist, and write a short receipt (stage, frameworks, platforms, sources read, `manifest-only`, unknowns, next action). Never open environment files, signing files or credentials during inspection. The receipt is a starting clue, not proof that a platform builds or a feature works. For an idea without a repository, skip it.
3. Choose the smallest relevant entry skill and detailed guide. Add another lead only when a handoff is needed. The eight commands are shortcuts, not a fixed process everyone must follow.
4. Take authorized, reversible steps that move the request forward. Ask one concise question only when a missing answer changes the next dependent action.

## Take the shortest route

These routes share the same public skills and command shortcuts. They do not add new mandatory stages. Use the actual request over any keyword hint. A focused fix does not need market research, onboarding questions or a new architecture proposal.

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

### Keyword routing hints

When the user has not named an intent or skill, use these hints to pick a first entry guide. They are hints only: the actual request and app evidence win.

**Scope check first.** If the request mentions a Chrome or browser extension, a Shopify app or humanizing text, and does not mention a mobile app, iOS or Android, it is probably another product. Use that product's workflow; confirm scope only if the request is ambiguous.

**Intent precedence.** Check the intents in this order and take the first one whose words appear in the request:

| Order | Intent | Words that suggest it | Entry guide | Next action |
| --- | --- | --- | --- | --- |
| 1 | resume | continue, resume, pick up | `guide-workflow-coordination` | Read the existing checkpoint, reconcile it with current files and resume its next unresolved action |
| 2 | fix | fix, repair, debug, crash, broken, error, hang, ANR | `guide-reliability` | Inspect the failing path, reproduce the defect, implement a focused repair and verify it |
| 3 | audit | audit | `guide-workflow-coordination` | Inspect relevant evidence, prioritize actionable findings and verify authorized fixes |
| 4 | review | review | `guide-workflow-coordination` | Review the selected change and affected checks; report findings without expanding scope |
| 5 | import | import, migrate data | `guide-workflow-coordination` | Inspect the supplied artifact and map it to the existing app without overwriting unrelated work |
| 6 | release | release, submit, publish, rollout | `guide-submission-rollout` | Check the exact candidate, platform evidence and owner-managed signing before an authorized release |
| 7 | research | research, validate idea, competitors, market demand | `guide-market-discovery` | Answer one product decision from available public evidence or supplied exports before account setup |
| 8 | grow | grow, growth, SEO, acquisition, retention | `guide-organic-growth` | Inspect the current funnel and evidence, then prepare one measurable growth improvement |
| 9 | design | design, screenshots, Figma, icon | `guide-platform-design` | Inspect the current screens and produce one reviewable design change for the actual platform |
| 10 | improve | improve, polish, onboarding | `guide-journeys-conversion` | Inspect the current journey, implement the smallest useful improvement and verify it |
| default | build (existing app) or research (idea) | none of the above | `guide-interface-media` or `guide-market-discovery` | Implement one observable slice in the existing stack, or answer one product decision |

**Build sub-routes.** When the intent is build, pick a more specific guide by topic (first match wins):

| Topic words | Entry guide |
| --- | --- |
| sign-in, login, authentication, auth, backend | `guide-auth-backend` |
| notification(s), subscription(s), billing | `guide-notifications-billing` |
| storage, offline, database, cache, state management | `guide-state-storage` |
| widget(s), watch, app clip, live activity | `guide-native-extensions` |
| anything else | `guide-interface-media` |

Detailed framework examples apply only when they match this app; never migrate an existing app to satisfy a guide.

## Use an inspection receipt

The [manual inspection checklist](EXECUTION-CONTRACT.md) describes which markers to read, the files never to open, the receipt fields and what to do when inspection is blocked. Inspection executes no project code, contacts no service and creates no persistent state beyond what the user agrees to keep. Preserve the receipt's task ID with the existing checkpoint when continuity is useful.

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

A focused fix needs a short result, changed behavior, affected checks and remaining limitation. A multi-finding audit, comparison, launch review or ongoing watch benefits from a written report. Gather the content from real evidence using the shape in [the report example](../templates/decision-report.json), then write the report yourself.

**Content limits** (keep these so reports stay scannable):

| Part | Limit |
| --- | --- |
| Title | Required, up to 120 characters |
| Project | Optional, up to 120 characters |
| Summary | Required, up to 1,000 characters |
| Signals | Up to 6, each a label and value of up to 80 characters |
| Findings | Up to 12, each with title (120), detail (700), optional evidence (250) and a status of `observed`, `attention`, `verified` or `unknown` (default `observed`) |
| Next actions | Up to 8, each with title (120), why (350) and a priority of `high`, `medium` or `low` (default `medium`) |
| Limits and unknowns | Up to 8 items of up to 300 characters |

**Format.** By default write a Markdown file in the user's project with the sections in this fixed order: Title, Summary, Signals (table), Findings (table with status and evidence), Next actions (table with priority), Limits and unknowns. When the host can display it (for example an artifact viewer, or a local file the user opens), you may write a single static HTML file instead.

**Rules for every report:**

1. Ask before overwriting an existing file; otherwise choose a new file name.
2. Before writing, check the content for secrets and remove any match. At minimum look for:

   | Pattern | Example of what it catches |
   | --- | --- |
   | `-----BEGIN ... PRIVATE KEY-----` (RSA, EC, OPENSSH or plain) | Private keys |
   | `sk-` followed by 16 or more letters, digits, `_` or `-` | OpenAI / Stripe-style secret keys |
   | `apify_api_` followed by 16 or more characters | Apify API tokens |
   | `ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_` followed by 20 or more characters | GitHub tokens |
   | `github_pat_` followed by 20 or more characters | GitHub fine-grained tokens |
   | Values from `.env` files, signing passwords, store API keys | Any credential |

3. In HTML, escape every piece of user-supplied or project-derived text: `&` as `&amp;`, `<` as `&lt;`, `>` as `&gt;`, `"` as `&quot;` and `'` as `&#39;`. Escape before inserting into any element or attribute.
4. HTML reports contain no `<script>`, no event-handler attributes, no remote fonts, images, stylesheets or trackers, and no forms. Inline CSS only.
5. Do not upload, publish or share the report. Check it for personal data and share only an authorized copy.
6. Show signals, findings, next actions and limits. Never substitute a visual score for missing verification; show a score only when it is backed by evidence.

Open or show the result for the user when the host supports it.

## Learn without hidden collection

At completion, make correction easy: point to the result and invite the user to name a wrong route, stale assumption, incomplete step or failed check. Do not insert a survey into every task. For feedback the user wants to share with the plugin publisher, use the [optional feedback route](FEEDBACK.md). Keep user-project feedback in that project unless the user explicitly submits it.

When a task is repeatable and the user requests ongoing help, use the [recurring-work recipes](RECURRING-WORK.md). Schedules belong to the user's host account; a plugin installation does not create one.
