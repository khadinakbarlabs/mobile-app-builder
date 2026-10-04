#!/usr/bin/env node
// Render a supplied, bounded report as a local HTML file; no network or scripts.
import fs from 'node:fs';
import path from 'node:path';

const MAX_BYTES = 128 * 1024;
const SENSITIVE = /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:sk-[A-Za-z0-9_-]{16,}|apify_api_[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b/;
const escapeHtml = value => String(value).replace(/[&<>"']/g, character => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
})[character]);

function requiredText(value, label, limit = 500) {
  if (typeof value !== 'string' || !value.trim() || value.length > limit || /[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(value)) {
    throw new Error(`${label} must be non-empty text below ${limit} characters`);
  }
  return value.trim();
}

function optionalText(value, label, limit = 500) {
  return value === undefined ? '' : requiredText(value, label, limit);
}

function boundedList(value, label, limit, validate) {
  if (value === undefined) return [];
  if (!Array.isArray(value) || value.length > limit) throw new Error(`${label} must have at most ${limit} items`);
  return value.map((item, index) => validate(item, `${label}[${index}]`));
}

function validate(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('Report must be a JSON object');
  if (SENSITIVE.test(JSON.stringify(input))) throw new Error('Report contains a sensitive value; remove it before rendering');
  const title = requiredText(input.title, 'title', 120);
  const summary = requiredText(input.summary, 'summary', 1000);
  const project = optionalText(input.project, 'project', 120);
  const signals = boundedList(input.signals, 'signals', 6, (item, label) => ({
    label: requiredText(item?.label, `${label}.label`, 80),
    value: requiredText(item?.value, `${label}.value`, 80),
  }));
  const findings = boundedList(input.findings, 'findings', 12, (item, label) => {
    const status = optionalText(item?.status, `${label}.status`, 24) || 'observed';
    if (!['observed', 'attention', 'verified', 'unknown'].includes(status)) throw new Error(`${label}.status is invalid`);
    return {
      title: requiredText(item?.title, `${label}.title`, 120),
      detail: requiredText(item?.detail, `${label}.detail`, 700),
      evidence: optionalText(item?.evidence, `${label}.evidence`, 250),
      status,
    };
  });
  const nextActions = boundedList(input.nextActions, 'nextActions', 8, (item, label) => {
    const priority = optionalText(item?.priority, `${label}.priority`, 16) || 'medium';
    if (!['high', 'medium', 'low'].includes(priority)) throw new Error(`${label}.priority is invalid`);
    return {
      title: requiredText(item?.title, `${label}.title`, 120),
      why: requiredText(item?.why, `${label}.why`, 350),
      priority,
    };
  });
  const limitations = boundedList(input.limitations, 'limitations', 8,
    (item, label) => requiredText(item, label, 300));
  return { title, summary, project, signals, findings, nextActions, limitations };
}

function metric(signal) {
  const percent = /^(100|[1-9]?\d)%$/.exec(signal.value);
  const bar = percent ? `<div class="meter" aria-hidden="true"><span style="width:${percent[1]}%"></span></div>` : '';
  return `<div class="metric"><span class="eyebrow">${escapeHtml(signal.label)}</span><strong>${escapeHtml(signal.value)}</strong>${bar}</div>`;
}

function render(report) {
  const findings = report.findings.map(item => `<article class="finding">
    <div class="row"><h3>${escapeHtml(item.title)}</h3><span class="badge ${item.status}">${escapeHtml(item.status)}</span></div>
    <p>${escapeHtml(item.detail)}</p>${item.evidence ? `<small>Evidence · ${escapeHtml(item.evidence)}</small>` : ''}
  </article>`).join('\n');
  const actions = report.nextActions.map((item, index) => `<li class="action">
    <span class="step">${index + 1}</span><div><div class="row"><h3>${escapeHtml(item.title)}</h3><span class="priority">${escapeHtml(item.priority)}</span></div><p>${escapeHtml(item.why)}</p></div>
  </li>`).join('\n');
  const limitations = report.limitations.map(item => `<li>${escapeHtml(item)}</li>`).join('\n');
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escapeHtml(report.title)} · Mobile App Builder</title>
<style>
:root{color-scheme:light;font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#152322;background:#f4f7f5}
*{box-sizing:border-box}body{margin:0;line-height:1.5}main{max-width:1120px;margin:auto;padding:28px 24px 70px}
.hero{border-radius:28px;padding:40px 44px;background:linear-gradient(125deg,#102e2b,#1d5b50 70%,#4c8a70);color:#fff;box-shadow:0 18px 40px #143f3426}
.eyebrow{text-transform:uppercase;letter-spacing:.13em;font-size:.72rem;font-weight:800}.hero .eyebrow{color:#afe8d1}h1{font-size:clamp(2rem,4vw,3.6rem);line-height:1.07;letter-spacing:-.045em;max-width:780px;margin:18px 0}h2{font-size:1.3rem;letter-spacing:-.02em;margin:0 0 18px}h3{font-size:1rem;margin:0;letter-spacing:-.01em}
.hero p{font-size:1.12rem;max-width:720px;color:#e0f3eb}.project{display:inline-block;border:1px solid #ffffff70;border-radius:99px;padding:5px 12px;font-size:.85rem;margin-top:18px}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:24px 0}.metric,.panel{background:#fff;border:1px solid #dce8e2;box-shadow:0 6px 18px #19362b0d;border-radius:18px}.metric{padding:18px 20px}.metric .eyebrow{color:#5b6f69}.metric strong{display:block;font-size:1.85rem;letter-spacing:-.04em;margin-top:6px}.meter{height:7px;border-radius:99px;background:#e5f1ea;margin-top:12px;overflow:hidden}.meter span{display:block;height:100%;background:#2d9c75;border-radius:99px}
.grid{display:grid;grid-template-columns:1.15fr .85fr;gap:18px}.panel{padding:25px}.finding{padding:16px 0;border-top:1px solid #e8eee9}.finding:first-of-type{border-top:0;padding-top:0}.finding p,.action p{margin:7px 0;color:#425550}.finding small{font-weight:600;color:#687b73}.row{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}.badge,.priority{flex:none;border-radius:99px;padding:3px 9px;font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;font-weight:800;background:#e7eee9;color:#38564a}.badge.attention{background:#fff1d8;color:#845c11}.badge.verified{background:#dff5e8;color:#236946}.badge.unknown{background:#eceef2;color:#566173}
.actions{padding:0;margin:0;list-style:none}.action{display:flex;gap:13px;padding:16px 0;border-top:1px solid #e8eee9}.action:first-child{border-top:0;padding-top:0}.step{display:grid;place-items:center;flex:none;width:27px;height:27px;border-radius:9px;background:#e5f3ea;color:#19704b;font-weight:800;font-size:.82rem}.priority{background:#e9f1eb;color:#3c6b52}
.limitations{margin-top:18px}.limitations ul{margin:0;padding-left:20px;color:#425550}.empty{color:#64756f;font-style:italic;margin:0}.foot{margin-top:24px;color:#718078;font-size:.76rem}
@media(max-width:760px){main{padding:14px 14px 44px}.hero{padding:28px 25px;border-radius:21px}.grid{grid-template-columns:1fr}.panel{padding:21px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;animation:none!important;transition:none!important}}
</style></head><body><main aria-label="Mobile App Builder report">
<header class="hero"><span class="eyebrow">Mobile App Builder · Decision report</span><h1>${escapeHtml(report.title)}</h1><p>${escapeHtml(report.summary)}</p>${report.project ? `<span class="project">${escapeHtml(report.project)}</span>` : ''}</header>
${report.signals.length ? `<section class="metrics" aria-label="Key signals">${report.signals.map(metric).join('')}</section>` : ''}
<div class="grid"><section class="panel" aria-label="Findings"><h2>What the evidence says</h2>${findings || '<p class="empty">No findings supplied.</p>'}</section>
<section class="panel" aria-label="Next actions"><h2>Next useful actions</h2>${actions ? `<ol class="actions">${actions}</ol>` : '<p class="empty">No actions supplied.</p>'}</section></div>
${limitations ? `<section class="panel limitations" aria-label="Limits and unknowns"><h2>Limits and unknowns</h2><ul>${limitations}</ul></section>` : ''}
<footer class="foot">Local report from user-supplied evidence. Recheck source, build, device and publication state separately.</footer></main></body></html>`;
}

function main() {
  const args = process.argv.slice(2);
  if (args.includes('--help')) {
    console.log('Usage: node scripts/render-report.mjs <report.json> --output <report.html>');
    return;
  }
  if (args.length !== 3 || args[1] !== '--output' || !args[2].endsWith('.html')) throw new Error('Usage: node scripts/render-report.mjs <report.json> --output <report.html>');
  const input = path.resolve(args[0]);
  const output = path.resolve(args[2]);
  const stat = fs.lstatSync(input);
  if (stat.isSymbolicLink() || !stat.isFile()) throw new Error('Input must be a regular JSON file');
  if (stat.size > MAX_BYTES) throw new Error('Input report exceeds the 128 KiB limit');
  let source;
  try { source = JSON.parse(fs.readFileSync(input, 'utf8')); }
  catch { throw new Error('Input must contain valid JSON'); }
  const html = render(validate(source));
  try { fs.writeFileSync(output, html, { flag: 'wx', mode: 0o600 }); }
  catch (error) {
    if (error.code === 'EEXIST') throw new Error('Output already exists; choose a new report path');
    throw error;
  }
  console.log(`Created local report: ${output}`);
}

try { main(); }
catch (error) { console.error(error.message); process.exitCode = 1; }
