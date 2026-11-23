---
name: build-web-app
description: "Build, improve and verify the web experience of an iOS, Android and web app. Use for responsive browser UI, web routes, static exports, accessibility, SEO, progressive web capabilities or a browser-specific bug in an existing app."
---

# Build the web experience

Start with the user's outcome and actual repository. Preserve existing features, visual direction, dirty changes, framework and SDK version. For a new project, record the intended iOS, Android and web targets and first useful feature before scaffolding. For an existing project, reproduce the affected browser interaction before editing. Do not replace a working stack just to use a preferred framework.

## Choose the implementation

Inspect package manifests, route structure, rendering mode, data/auth boundaries and existing tests. Reuse shared product logic where practical and isolate native-only modules behind platform adapters. When the project uses Expo, check the [official web guide](https://docs.expo.dev/workflow/web/) and the documentation matching its actual SDK; the original mobile scaffold has an SDK 54 baseline, not a mandate to upgrade an existing app. Framework-specific commands belong in the consuming project after checking its package manager and authorization.

For Expo web, check the appropriate react-dom, react-native-web and web runtime dependencies, start the web development server using the installed Expo CLI, and prepare the project's configured web export with `npx expo export --platform web`. Choose client, static or server rendering according to actual route/data requirements. Verify the installed router's guidance before adding static generation or server APIs. For another stack, use that framework's current official docs and build pipeline. A successful export does not prove a deployed site.

## Build a useful vertical slice

Implement the real screen, loading, empty, error and retry states. Test deep-link refresh, history/back navigation and missing routes. Adapt layout for small phones, tablets and desktop without changing the product's established direction. Provide semantic landmarks, keyboard access, visible focus, accessible names, sufficient contrast and reduced-motion behavior. Avoid a screen made only of oversized mobile components on desktop.

Keep server secrets out of browser bundles and public environment variables. Use the existing authentication boundary and explicit authorization on server operations. Check input validation, output encoding, trusted redirect destinations and cross-origin/session handling where relevant. Do not invent payment, account or storage integrations. Use server-side access when required rather than exposing provider credentials to the browser.

For indexable public pages, verify titles, descriptions, canonical URLs, robots rules and sitemap coverage against the actual deployment. Preserve noindex and authentication for private dashboards. Add a manifest, offline behavior or service worker only when the product needs it; verify update/caching behavior and do not label a site as an installed PWA without proof.

## Verify and report

Run the consuming project's relevant type, lint, build and behavioral checks. Test the changed user journey in a real browser at representative phone, tablet and desktop widths, including keyboard navigation. Capture browser console/network failures and resolve errors affecting the journey. Check iOS/Android impacts when shared code changes. Verify deployed routes only when deployment is authorized and actually completed.

Return the changed behavior, files, test evidence and precise remaining gates. Keep source checks, local browser interaction, export, deployed URL and native device evidence separate. A workflow package release does not prove a consumer app is deployed or accepted by a store.
