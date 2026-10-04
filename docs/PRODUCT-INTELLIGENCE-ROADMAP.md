# Mobile App Builder: context, learning and recurring value

Status: local-first phase implemented for 2.3.0 on 2026-10-05; connected analytics and automatic scheduling remain proposals. This roadmap adds no discoverable skills, commands, agents, hooks, connectors or telemetry.

## Product outcome

Help a person move an app forward with less repeated explanation. For a new idea, return the smallest defensible next decision. For an existing app, inspect its actual state, preserve prior decisions and complete the next useful task. For either route, make the result and evidence easy to assess. Repeat work only when the user chooses a recurring outcome.

The current package already has 30 entry skills, eight commands, eight lead agents and 190 detailed guides. Its commands name fixed entry skills, and its catalog helper filters prepared metadata by department, platform and substring. The first upgrade should improve context capture and selection within those components, rather than increase the component count.

## 1. A compact, user-owned project context

The first task creates or updates a small context card in the consuming project when a durable record would help. Prefer the project's existing planning system; otherwise use a clearly named, reviewable Markdown file. Do not create a hidden data store. Record only:

- product purpose, audience, maturity, target platforms and current stack;
- the user's immediate outcome and constraints;
- established design and architecture decisions, with source and date;
- observed signals, hypotheses and unknowns kept separate;
- last verified source/build/device/store state;
- the next recommended action and why it outranks alternatives.

Do not copy session transcripts, raw analytics, credentials, customer records or private research datasets into this card. Refresh a field only from current evidence or an explicit user correction; keep stale fields marked stale. Existing repository instructions and local project context take precedence.

## 2. An outcome router with bounded initiative

The existing coordination skill and commands should follow one short decision path:

1. Classify the starting point: idea, existing app, or one focused task.
2. Identify the user-visible outcome and the decision that would unblock it.
3. Inspect available project context before asking for information.
4. Choose one lead and only the detailed guides needed for the next action.
5. State a confidence level and the evidence or missing fact behind it.
6. Perform authorized, reversible preparation and verification; ask one concise question only when its answer changes the next action.
7. Return the result, evidence, remaining uncertainty and next useful move.

For example, “my onboarding feels weak” in a working app should inspect the real onboarding journey and available activation evidence, then route design, implementation and behavior QA as needed. It should not start a generic market study or replace the existing app. “I have an idea for a budget app” should validate the user problem and first useful journey before choosing architecture.

The router should be evaluated with positive, negative and ambiguous prompts. Measure whether it chose the right guide, avoided unnecessary questions, preserved context and produced an assessable result. A high-confidence route is a hypothesis backed by project evidence, not a claim that the agent has instinctive knowledge.

## First-use and return experience

Make the first interaction work from ordinary language: “I have an idea,” “Here is my app,” or “Help me with this one problem.” Show a useful first result before suggesting setup. The current eight commands remain shortcuts, not prerequisites. After the result, suggest at most one follow-up that matches the user's project stage, such as testing the first journey, checking a release blocker or monitoring a competitor change.

Improve public examples around completed jobs: idea to evidence-backed first feature, existing-app bug to verified fix, and store listing to a truthful asset set. Keep the examples short enough to copy and include the expected output. This should improve discovery-to-first-value conversion without adding another agent or command.

## 3. Feedback that improves the product

Use three separate signal sources:

| Signal | Collection path | Interpretation |
| --- | --- | --- |
| Explicit feedback | Optional “Was this useful? What was missing?” prompt and a public issue/form link | Qualitative product evidence, not a full-session transcript |
| Local task outcome | User-visible acceptance and verification recorded in the user's project | Evidence for that project; not automatically reported to the publisher |
| Aggregate distribution | Directory or repository metrics, if the publisher surface actually provides them | Reach and adoption, not proof of user value |

Classify feedback into wrong route, repeated question, stale context, inaccurate source, incomplete implementation, failed verification and missing capability. Maintain a small regression prompt for each confirmed recurring problem. Triage feedback by user impact and recurrence; publish fixes with before/after behavior and exact validation. Never silently transmit project contents or session text to a publisher endpoint. Any future product telemetry requires a separate, disclosed opt-in design, data-minimization review and a way to disable it.

## 4. Scheduled work tied to a result

Offer schedules only when a person asks for a recurring outcome or chooses one after seeing a useful one-time result. Suggested recipes:

- Weekly app health: changed errors, broken journeys, release risks and one prioritized fix.
- Store and competitor watch: only meaningful listing, review or positioning changes, with dated sources.
- SEO and discoverability: changed technical issues, search opportunities and evidence-backed actions.
- Pre-release check: build identity, current CI, device evidence and outstanding store gates.

Each saved routine needs an explicit project, cadence, timezone, data sources, permitted tools, spend ceiling, output destination, pause/delete path and success condition. Keep unchanged runs quiet. Start with read-only summaries or draft pull requests; do not allow a recurring run to spend on research, contact people, deploy, publish or modify store accounts by default. A green infrastructure run is not evidence that the underlying task succeeded.

Claude Code currently offers account-owned cloud Routines with schedule, API and GitHub triggers, plus local Desktop scheduled tasks. Cloud routines run as autonomous sessions and may use the repositories and connectors granted to them. Keep each routine narrowly scoped. This is a host capability, not a background service bundled into Mobile App Builder. See [Routines](https://code.claude.com/docs/en/routines) and [Desktop scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks).

## 5. Measure useful repeat use

Track the funnel only where each signal is actually available:

1. Discovery and install: directory or repository aggregates, if exposed.
2. First useful result: a user confirms that a concrete decision, artifact or fix helped.
   Review the time and number of questions required to reach it in opted-in usability tests.
3. Completion quality: accepted task outcome with the appropriate source/build/device evidence.
4. Repeat value: distinct useful tasks over time, rather than raw session count.
5. Scheduled value: opted-in routines that surfaced an actionable change, with false-alert rate and time saved.

Do not infer invocation, retention or satisfaction from install counts. A skills-only plugin has no publisher-owned session telemetry today. If first-party product analytics later becomes necessary, build it as an optional, transparent companion service with user accounts and an explicit privacy contract; keep the core usable without it.

## Build order and review gates

1. **Local-first intelligence:** context-card format, routing rules within existing commands/coordination skill, and a scenario evaluation set. Keep the package within the current component budget.
2. **Feedback loop:** public feedback path, regression taxonomy and a repeatable review process. Verify that private project data is never included by default.
3. **Schedules:** document and test one narrow, user-owned read-only routine recipe. Verify actual run outputs and pause behavior before offering more recipes.
4. **Optional connected product:** consider durable accounts, opt-in analytics and richer schedules only after evidence of repeat value and a reviewed data-handling design.

The local-first context, routing, visual report, optional feedback route and schedule recipes are implemented in 2.3.0. No schedule or publisher telemetry starts on installation. Treat package checks, exact published source, directory review and live availability as separate states.
