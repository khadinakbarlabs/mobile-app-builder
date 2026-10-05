#!/usr/bin/env node
// Inspect only public project markers; never execute project code or read secrets.
import fs from 'node:fs';
import path from 'node:path';
import { randomUUID } from 'node:crypto';
import { intents, routeTask } from './task-route.mjs';

const MAX_MANIFEST_BYTES = 128 * 1024;
const helperVersion = '1.1.0';
const runId = randomUUID();
let taskId = null;

function fault(code, message, recovery) {
  return Object.assign(new Error(message), { safeCode: code, recovery });
}

function entry(root, name, kind) {
  const file = path.join(root, name);
  let stat;
  try { stat = fs.lstatSync(file); }
  catch (error) {
    if (error.code === 'ENOENT') return null;
    throw error;
  }
  if (stat.isSymbolicLink()) throw fault('SYMLINK_REQUIRES_REVIEW',
    `${name} is a symbolic link; inspect it manually`, 'Select a verified regular project marker; do not follow links automatically');
  if (kind === 'file' && !stat.isFile()) throw fault('INVALID_PROJECT', `${name} must be a regular file`, 'Inspect the selected project marker');
  if (kind === 'directory' && !stat.isDirectory()) throw fault('INVALID_PROJECT', `${name} must be a regular directory`, 'Inspect the selected project directory');
  return { file, stat };
}

function readJson(root, name) {
  const found = entry(root, name, 'file');
  if (!found) return null;
  if (found.stat.size > MAX_MANIFEST_BYTES) throw fault('MANIFEST_TOO_LARGE',
    `${name} exceeds the 128 KiB inspection limit`, 'Review the manifest manually; no source was executed');
  let descriptor;
  try {
    descriptor = fs.openSync(found.file, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW ?? 0));
    const info = fs.fstatSync(descriptor);
    if (!info.isFile()) throw fault('INVALID_MANIFEST', `${name} must be a regular file`, 'Review the manifest');
    if (info.size > MAX_MANIFEST_BYTES) throw fault('MANIFEST_TOO_LARGE', `${name} exceeds the inspection limit`, 'Review the manifest manually');
    const buffer = Buffer.alloc(MAX_MANIFEST_BYTES + 1);
    let count = 0;
    while (count < buffer.length) {
      const size = fs.readSync(descriptor, buffer, count, buffer.length - count, null);
      if (!size) break;
      count += size;
    }
    if (count > MAX_MANIFEST_BYTES) throw fault('MANIFEST_TOO_LARGE', `${name} exceeds the inspection limit`, 'Review the manifest manually');
    try {
      const value = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(buffer.subarray(0, count)));
      if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error();
      return value;
    } catch { throw fault('INVALID_MANIFEST', `${name} is not a valid JSON object`, 'Fix the selected manifest without discarding unrelated work, then inspect again'); }
  } finally { if (descriptor !== undefined) fs.closeSync(descriptor); }
}

function parseArgs(argv) {
  if (argv.includes('--help')) {
    console.log('Usage: node scripts/inspect-project.mjs <project-directory> [--goal "outcome"] [--intent ' + intents.join('|') + '] [--task-id id]');
    return null;
  }
  if (!argv.length || argv[0].startsWith('--')) throw fault('INVALID_INPUT', 'Select a project directory', 'Pass a project directory; use --help for supported options');
  const [directory, ...rest] = argv;
  const values = new Map();
  for (let index = 0; index < rest.length; index += 2) {
    const key = rest[index];
    const value = rest[index + 1];
    if (!['--goal', '--intent', '--task-id'].includes(key) || values.has(key) || !value || value.startsWith('--')) {
      throw fault('INVALID_INPUT', 'Use each supported option once with a value', 'Use --help and correct the input; nothing was changed');
    }
    values.set(key, value);
  }
  const goal = values.get('--goal') ?? null;
  if (goal !== null && (goal.length > 200 || /[\x00-\x1f\x7f]/.test(goal))) {
    throw fault('INVALID_INPUT', 'Goal must be one line of at most 200 characters', 'Provide a concise non-sensitive outcome');
  }
  const intent = values.get('--intent') || 'auto';
  if (!intents.includes(intent)) throw fault('INVALID_INPUT', 'Unsupported intent', 'Choose an intent listed by --help');
  const selectedTask = values.get('--task-id');
  if (selectedTask && !/^[a-z0-9][a-z0-9-]{0,79}$/.test(selectedTask)) throw fault('INVALID_INPUT', 'Task ID must be a short lowercase identifier', 'Reuse a non-sensitive task ID or omit it');
  taskId = selectedTask || runId;
  return { directory: path.resolve(directory), goal, intent };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args) return;
  const { directory, goal, intent } = args;
  let root;
  try { root = fs.lstatSync(directory); }
  catch (error) {
    if (error.code === 'ENOENT') throw fault('PROJECT_NOT_FOUND', 'Selected project was not found', 'Locate the existing app directory and retry; do not create a replacement app');
    throw error;
  }
  if (root.isSymbolicLink() || !root.isDirectory()) throw fault('INVALID_PROJECT', 'Project root must be a regular directory', 'Select the verified app directory');
  const packageFile = readJson(directory, 'package.json');
  const appFile = readJson(directory, 'app.json');
  const pubspec = entry(directory, 'pubspec.yaml', 'file');
  const ios = entry(directory, 'ios', 'directory');
  const android = entry(directory, 'android', 'directory');
  const gradle = ['build.gradle', 'build.gradle.kts', 'settings.gradle', 'settings.gradle.kts'].filter(name => entry(directory, name, 'file'));
  const instructionFiles = ['AGENTS.md', 'CLAUDE.md'].filter(name => entry(directory, name, 'file'));
  const dependencies = { ...(packageFile?.dependencies || {}), ...(packageFile?.devDependencies || {}) };
  const scripts = packageFile?.scripts && typeof packageFile.scripts === 'object' && !Array.isArray(packageFile.scripts) ? packageFile.scripts : {};
  const frameworks = [];
  if (dependencies.expo || appFile?.expo) frameworks.push('Expo');
  else if (dependencies['react-native']) frameworks.push('React Native');
  if (pubspec) frameworks.push('Flutter');
  if (dependencies.next) frameworks.push('Next.js');
  if (dependencies.vite) frameworks.push('Vite');
  if (dependencies['@angular/core']) frameworks.push('Angular');
  if (dependencies['@sveltejs/kit']) frameworks.push('SvelteKit');
  if (gradle.length && !frameworks.some(name => ['Expo', 'React Native', 'Flutter'].includes(name))) frameworks.push('Native Android');
  if (ios && !frameworks.some(name => ['Expo', 'React Native', 'Flutter'].includes(name))) frameworks.push('Native iOS');
  const platforms = [];
  if (ios || frameworks.includes('Expo') || frameworks.includes('React Native') || pubspec) platforms.push('ios');
  if (android || gradle.length || frameworks.includes('Expo') || frameworks.includes('React Native') || pubspec) platforms.push('android');
  if (dependencies['react-native-web'] || frameworks.some(name => ['Next.js', 'Vite', 'Angular', 'SvelteKit'].includes(name)) || scripts.web) platforms.push('web');
  const availableChecks = ['lint', 'test', 'typecheck', 'check'].filter(name => typeof scripts[name] === 'string' && scripts[name].trim());
  const sources = [];
  if (packageFile) sources.push('package.json');
  if (appFile) sources.push('app.json');
  if (pubspec) sources.push('pubspec.yaml');
  if (ios) sources.push('ios/');
  if (android) sources.push('android/');
  sources.push(...gradle);
  const stage = sources.length ? 'existing-app' : 'idea-or-unknown';
  const route = routeTask(goal, intent, stage === 'existing-app');
  const report = {
    schemaVersion: 2, operation: 'inspect-project', state: 'completed',
    identity: { helper: 'inspect-project', helperVersion, runId, taskId },
    observedAt: new Date().toISOString(),
    capability: { runtime: 'Node.js', runtimeVersion: process.versions.node, access: 'local-read-only',
      reads: 'bounded public project markers', accountRequired: false, projectCodeExecuted: false },
    project: path.basename(directory), requestedOutcome: goal, stage, platforms, frameworks,
    availableChecks, sources, instructionFiles, route,
    verification: { level: 'manifest-only', platformSupport: 'inferred', checksExecuted: [], buildExecuted: false, deviceObserved: false, externalOutcome: 'not-run' },
    unknowns: stage === 'existing-app'
      ? ['Audience and success measure require user or project evidence', 'Working behavior, executable availability and device status are unverified']
      : ['No supported app manifest was found', 'Audience, platforms and first useful outcome are unverified'],
    nextStep: route.nextAction,
    continuation: { taskId, checkpoint: 'Use the consuming project’s existing context card or issue; this helper creates no persistent state', nextAction: route.nextAction },
  };
  console.log(JSON.stringify(report, null, 2));
}

try { main(); }
catch (error) {
  const fallback = error.code === 'EACCES' || error.code === 'EPERM'
    ? ['ACCESS_DENIED', 'Selected project access was denied', 'Use an authorized readable app directory']
    : ['LOCAL_IO_ERROR', 'Local inspection could not complete', 'Inspect the selected public markers manually; nothing was changed'];
  const [code, message, recovery] = error.safeCode ? [error.safeCode, error.message, error.recovery] : fallback;
  console.log(JSON.stringify({ schemaVersion: 2, operation: 'inspect-project', state: 'blocked',
    identity: { helper: 'inspect-project', helperVersion, runId, taskId },
    error: { code, message, recovery }, verification: { level: 'none', projectCodeExecuted: false },
    continuation: { nextAction: recovery } }, null, 2));
  console.error(`${code}: ${message}`);
  process.exitCode = 1;
}
