# Mobile App Builder 2.4.0 evaluation

Evaluation checkpoint: October 6, 2026. Machine-readable evidence: [evaluation-2.4.0.json](evaluation-2.4.0.json). Cases and fixtures: [reviewer-cases.json](reviewer-cases.json). This report records source and local-host evidence before the new GitHub release and directory scan; it does not establish directory approval.

## Gaps verified against the baseline

The canonical baseline was `a98b356`, version 2.3.9. Some entry descriptions described general topics rather than user tasks; focused repair and resume requests lacked an explicit execution route. The local inspector returned useful framework hints but lacked structured recovery codes, task identity and verification limits. Existing local editions were stale or absent. Several copyable signing and session examples referenced private files or stored sessions even though the core prohibits reading installer credentials. The directory's earlier scan passed policy with a credential warning and remained in review.

## Implemented changes

- Task-oriented discovery, explicit build/fix/audit/improve/import/review/release/resume routes, short first-result milestones and stack preservation.
- Read-only inspector 1.1.0: bounded public markers, task/run identity, safe errors, provenance, continuation and explicit manifest-only verification.
- Owner-managed signing and session adapters; no private credential-file upload examples. Regression checks reject these examples. The optional research integration and isolated public CLI search remain available.
- Shared checkpoints, reconciliation before repeating an unknown external action, optional feedback and host-specific schedule activation/readback guidance. No recurring task was activated by this upgrade.
- Separate native packages with full resource closure: 30 core skills, eight commands and eight agents; Codex preserves the commands as eight skill aliases. The 189 original workflows and 16 original role cards remain accessible.

## Executed checks

| Check | Result | Evidence and limit |
| --- | --- | --- |
| Regression suite | Passed, 42/42 | Local routing, bounded inspection, safe errors, report escaping, credential boundaries, migration and native resource checks |
| Plugin Builder preflight | Passed | Component budget and generated Codex validation; no errors or warnings |
| Official strict manifests | Passed | Marketplace, core and research; CLI 2.1.287 |
| Archive integrity | Passed | File inventories, contained resources and hash readback for separate host packages |
| Codex discovery | Passed, 38/38 | App-server 0.146.0 exposes enabled 2.4.0 skills, including eight aliases |
| Claude Code discovery | Passed | 38 skill/command entries and eight agents; installed 2.4.0 enabled |
| Cursor discovery | Passed | Customize shows 2.4.0 with 30 skills, eight commands and eight agents |
| Claude native-model evaluation | Blocked | Local CLI is not signed in |
| Device/simulator verification | Not run | Source and mocked checks do not establish a rendered app journey |
| Authenticated research | Not run | Public CLI discovery is separate from a paid authenticated Actor run |

Codex and Claude Code use supported installation flows. Cursor uses the native local plugin folder. Unchanged legacy Cursor shortcuts retain their IDs and point to the current guides; unrelated shortcuts were preserved. A new session is needed to refresh an already-open host's skill context.

## Same-fixture comparison

One synthetic rejected-login spinner fixture was run in two isolated Codex configurations, with Mobile App Builder enabled and disabled. The observed model was `gpt-5.6-sol` on CLI 0.146.0; an earlier attempt with the configured `gpt-6.1-sol` was blocked because that model was unavailable to the stock CLI account. The configured model was not silently reported as the observed model.

Both completed the repair: **1/1 outcome and 2/2 Node checks per configuration**, zero unnecessary questions, preserved stack, and explicit missing device evidence. The enabled run did not visibly read a plugin skill. A later isolated explicit attempt confirmed that `--ignore-user-config` suppresses plugin exposure in this CLI despite the enabled flag; the model disclosed the unavailable skill and repaired the fixture directly. Successful plugin attribution or a quality improvement in the paired comparison is therefore **not established**. Durations were approximately 54 seconds enabled and 59 seconds disabled; different output modes and a recovered baseline path alias confound those timings, so no efficiency gain is claimed. Cost was not measured.

A separate explicit invocation in the configured host **selected and read the installed improve-app and reliability skills**, but did not complete within a 180-second bound; repeated host hook failures were observed. Its completion is Blocked. An isolated fallback completed the same two Node checks in approximately 46 seconds while disclosing that the plugin was unavailable. Neither attempt establishes an end-to-end plugin benefit. User-wide hook/configuration troubleshooting was not applied to unrelated settings.

## Representative-case coverage

| Case | Native-model execution | Other evidence |
| --- | --- | --- |
| Explicit login repair | Blocked at runtime bound; skill selection/read passed | Prompt variant and isolated fallback passed two mocked checks each without verified plugin attribution |
| Indirect Flutter crash | Not run | Flutter fix routing and stack preservation pass locally; no actual crash fixture execution |
| Supplied design import | Not run | Reviewable fixture and acceptance prepared |
| Resume checkpoint | Not run | Deterministic resume route and guidance checked |
| Unknown upload | Not run | Reconcile-before-retry guidance reviewed; no external upload |
| Other product | Not run | Chrome-extension request stays outside mobile routing |
| Invalid manifest | Not run | Structured error, no private content echo, original file preserved |
| Missing runtime/account | Not run | Manual/public fallback guidance reviewed |

Zero of eight exact prepared cases completed end to end with verified plugin exposure: one was attempted and blocked after successful skill selection, and seven were not run. The paired prompt variant completed one synthetic fixture in both configurations. Deterministic helper checks cover several additional routes but are separate evidence. No aggregate success rate across all eight, user-session uplift, authenticated integration result or live directory availability is claimed.

## Publication boundary and next step

The new source must be pushed, its CI checked, and the exact new directory version scanned before declaring the credential warning resolved. Preserve the existing OpenAI review when its portal does not permit a pending-version replacement. Human review and live availability remain separate from source validation. The next behavioral step is an authenticated native evaluation of the eight prepared cases, followed by an affected real device journey.
