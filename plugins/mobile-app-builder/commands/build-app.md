---
description: "Build a focused app feature for the project’s actual stack."
argument-hint: "feature and platform"
---

# build-app

Apply [the context and reporting workflow](../docs/INTELLIGENT-WORKFLOW.md). Identify the first observable result, inspect the current stack and report what behavior is actually verified.

Read only the entry skills relevant to the request: [guide-architecture-tooling](../skills/guide-architecture-tooling/SKILL.md), [guide-interface-media](../skills/guide-interface-media/SKILL.md), [guide-auth-backend](../skills/guide-auth-backend/SKILL.md), [guide-state-storage](../skills/guide-state-storage/SKILL.md), [guide-native-extensions](../skills/guide-native-extensions/SKILL.md).

Inspect the real stack and constraints; select only relevant implementation guides; implement one vertical slice; test its affected behavior on all affected platforms.

For a repair, use the reliability route and reproduce the failing path first. For a review, report findings without unrelated implementation. Resume an existing checkpoint before planning a new feature. Do not load the architecture guide for an isolated UI or auth fix unless the observed cause requires it.

Start from the context the user provides. Ask only for a missing fact that changes the next action; continue independent work. Preserve unrelated changes. Paid research, account operations, deployments and publication follow the user's actual authorization.

Finish with the result, verification evidence, limitations and next concrete action.
