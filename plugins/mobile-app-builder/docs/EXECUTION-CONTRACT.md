# Local inspection contract

`inspect-project` helper 1.1.0 emits one JSON document on stdout. Diagnostics go to stderr. Exit 0 means the bounded manifest inspection completed; exit 1 means it is blocked. Neither establishes a working app, available toolchain or device test.

## Inputs and access

Select one existing regular project directory. Optional `--goal` is a non-sensitive single line of at most 200 characters. `--intent` accepts `auto`, `build`, `fix`, `audit`, `improve`, `import`, `review`, `release`, `resume`, `research`, `design` or `grow`. Explicit intent takes precedence. `--task-id` accepts a lowercase identifier of at most 80 characters; omit it for a fresh ID. Pass each option once.

The helper reads `package.json` and `app.json` as bounded JSON objects, each at most 128 KiB. It checks only the presence of public framework and instruction markers. It refuses symbolic-link markers, does not echo arbitrary manifest fields or script bodies, and never reads environment files, private keys, app sessions or installer credentials. The project basename and supplied goal are returned, so use non-sensitive names. It requires only Node.js and installs nothing.

## Result fields

| Field | Meaning |
| --- | --- |
| `schemaVersion`, `operation`, `state` | Version 2; `inspect-project`; `completed` or `blocked` |
| `identity` | Helper/version, a new run ID and the supplied or generated task ID |
| `capability` | Runtime/version, bounded local access and no project execution |
| `observedAt`, `sources` | Snapshot timestamp and selected marker identities |
| `stage`, `frameworks`, `platforms` | Inferred app shape; verify against the actual code before acting |
| `route` | Explicit route or keyword hint, applicable entry skill and stack-preservation policy |
| `verification` | `manifest-only`; no checks, build, device or external action performed |
| `unknowns`, `continuation` | Missing evidence and one action to carry into the existing project checkpoint |

Keep old top-level `project`, `requestedOutcome`, `availableChecks` and `nextStep` readers working. New fields are additive; consumers should ignore unknown fields. `scope: other-product` is a hint to choose another product workflow, not a failed inspection.

## Safe errors and recovery

| Code | Next action |
| --- | --- |
| `INVALID_INPUT` | Correct the bounded arguments; use `--help` |
| `PROJECT_NOT_FOUND` | Locate the existing app; do not scaffold a replacement |
| `INVALID_PROJECT` | Select a verified regular directory/marker |
| `INVALID_MANIFEST` | Repair the selected JSON without discarding unrelated work |
| `MANIFEST_TOO_LARGE` | Inspect that manifest manually |
| `SYMLINK_REQUIRES_REVIEW` | Review the link and intended target manually |
| `ACCESS_DENIED` | Use an authorized readable project |
| `LOCAL_IO_ERROR` | Inspect public markers manually; no changes were made |

The helper owns no authenticated or external operation, so it never produces an authentication, partial-upload or unknown-external-action result. The active agent must record those states separately when using an authorized service. Do not convert an external timeout into a success or repeat the action before reconciliation.
