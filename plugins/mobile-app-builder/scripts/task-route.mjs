// Local routing hints. The active agent still reconciles the user's actual intent.
export const intents = ['auto', 'build', 'fix', 'audit', 'improve', 'import', 'review', 'release', 'resume', 'research', 'design', 'grow'];

const routes = {
  build: ['guide-interface-media', 'Implement one observable slice in the existing stack, then run its affected checks'],
  fix: ['guide-reliability', 'Inspect the failing path, reproduce the defect, implement a focused repair and verify it'],
  audit: ['guide-workflow-coordination', 'Inspect relevant evidence, prioritize actionable findings and verify authorized fixes'],
  improve: ['guide-journeys-conversion', 'Inspect the current journey, implement the smallest useful improvement and verify it'],
  import: ['guide-workflow-coordination', 'Inspect the supplied artifact and map it to the existing app without overwriting unrelated work'],
  review: ['guide-workflow-coordination', 'Review the selected change and affected checks; report findings without expanding scope'],
  release: ['guide-submission-rollout', 'Check the exact candidate, platform evidence and owner-managed signing before an authorized release'],
  resume: ['guide-workflow-coordination', 'Read the existing checkpoint, reconcile it with current files and resume its next unresolved action'],
  research: ['guide-market-discovery', 'Answer one product decision from available public evidence or supplied exports before account setup'],
  design: ['guide-platform-design', 'Inspect the current screens and produce one reviewable design change for the actual platform'],
  grow: ['guide-organic-growth', 'Inspect the current funnel and evidence, then prepare one measurable growth improvement'],
};

export function routeTask(goal, requested, existing) {
  const text = (goal || '').toLowerCase();
  if (requested === 'auto' && /\b(chrome extension|browser extension|shopify app|humaniz[ei])\b/.test(text)
      && !/\b(mobile app|ios|android)\b/.test(text)) {
    return { intent: 'scope-check', selection: 'keyword-hint', scope: 'other-product', entrySkill: null,
      stackPolicy: 'preserve', nextAction: 'Use the appropriate product workflow; confirm scope only if the request is ambiguous',
      limitations: ['A keyword hint does not establish which product the user intends'] };
  }
  let intent = requested;
  if (intent === 'auto') {
    const candidates = [
      ['resume', /\b(continue|resume|pick up)\b/],
      ['fix', /\b(fix|repair|debug|crash|broken|error|hang|anr)\b/],
      ['audit', /\baudit\b/], ['review', /\breview\b/],
      ['import', /\b(import|migrate data)\b/],
      ['release', /\b(release|submit|publish|rollout)\b/],
      ['research', /\b(research|validate idea|competitors|market demand)\b/],
      ['grow', /\b(grow|growth|seo|acquisition|retention)\b/],
      ['design', /\b(design|screenshots|figma|icon)\b/],
      ['improve', /\b(improve|polish|onboarding)\b/],
    ];
    intent = candidates.find(([, pattern]) => pattern.test(text))?.[0] || (existing ? 'build' : 'research');
  }
  let [entrySkill, nextAction] = routes[intent];
  if (intent === 'build') {
    const topics = [
      ['guide-auth-backend', /\b(sign[ -]?in|log[ -]?in|authentication|auth|backend)\b/],
      ['guide-notifications-billing', /\b(notification|notifications|subscription|subscriptions|billing)\b/],
      ['guide-state-storage', /\b(storage|offline|database|cache|state management)\b/],
      ['guide-native-extensions', /\b(widget|widgets|watch|app clip|live activity)\b/],
    ];
    entrySkill = topics.find(([, pattern]) => pattern.test(text))?.[0] || entrySkill;
  }
  return { intent, selection: requested === 'auto' ? 'keyword-hint' : 'explicit', scope: 'app', entrySkill,
    stackPolicy: 'preserve', nextAction,
    limitations: ['Routing is a local hint; reconcile it with the actual request and app evidence',
      'Detailed framework examples apply only when they match this app; never migrate an existing app to satisfy a guide'] };
}
