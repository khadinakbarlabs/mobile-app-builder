---
description: "Discover public research Actors with the installed Apify CLI before choosing a bounded mobile research route."
argument-hint: "research topic"
---

# Research Actors with the CLI

Use the installed Apify CLI to discover public Actors for the user's stated mobile research question. Run `node scripts/actor-search.mjs --query "<topic>" --limit 5` from this plugin root when a local shell and Apify CLI are available. The bundled script isolates the CLI from ambient account credentials and disables its update check and telemetry for this search. It does not run an Actor or read an account token. If the CLI is unavailable, use the declared research connection's search tool when configured, or produce a search plan.

Inspect the returned Actor's current schema, pricing, source coverage, rights and useful output before recommending or running it. The search result is discovery evidence, not proof of fitness, cost, or a completed run. For an authenticated run, follow the [research connection workflow](../skills/research-connection/SKILL.md); the core package also includes an owner-operated CLI workflow. Do not inspect or reuse the CLI's saved login on the assistant's behalf. Record exact run and dataset IDs only after an authorized execution.
