#!/usr/bin/env node
// Read a few public project manifests and return a bounded context snapshot.
import fs from 'node:fs';
import path from 'node:path';

const MAX_MANIFEST_BYTES = 128 * 1024;

function entry(root, name, kind) {
  const file = path.join(root, name);
  let stat;
  try { stat = fs.lstatSync(file); }
  catch (error) {
    if (error.code === 'ENOENT') return null;
    throw error;
  }
  if (stat.isSymbolicLink()) throw new Error(`${name} is a symbolic link; inspect it manually`);
  if (kind === 'file' && !stat.isFile()) throw new Error(`${name} must be a regular file`);
  if (kind === 'directory' && !stat.isDirectory()) throw new Error(`${name} must be a regular directory`);
  return { file, stat };
}

function readJson(root, name) {
  const found = entry(root, name, 'file');
  if (!found) return null;
  if (found.stat.size > MAX_MANIFEST_BYTES) throw new Error(`${name} exceeds the 128 KiB inspection limit`);
  try {
    const value = JSON.parse(fs.readFileSync(found.file, 'utf8'));
    if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error();
    return value;
  } catch { throw new Error(`${name} is not a valid JSON object`); }
}

function parseArgs(argv) {
  if (!argv.length || argv.includes('--help')) {
    console.log('Usage: node scripts/inspect-project.mjs <project-directory> [--goal "user outcome"]');
    process.exit(argv.includes('--help') ? 0 : 1);
  }
  const [directory, ...rest] = argv;
  let goal = null;
  for (let index = 0; index < rest.length; index++) {
    if (rest[index] !== '--goal' || goal !== null || !rest[index + 1]) throw new Error('Use one --goal with a short outcome');
    goal = rest[++index];
  }
  if (goal !== null && (goal.length > 200 || /[\x00-\x1f\x7f]/.test(goal))) {
    throw new Error('Goal must be one line of at most 200 characters');
  }
  return { directory: path.resolve(directory), goal };
}

function main() {
  const { directory, goal } = parseArgs(process.argv.slice(2));
  const root = fs.lstatSync(directory);
  if (root.isSymbolicLink() || !root.isDirectory()) throw new Error('Project root must be a regular directory');
  const packageFile = readJson(directory, 'package.json');
  const appFile = readJson(directory, 'app.json');
  const pubspec = entry(directory, 'pubspec.yaml', 'file');
  const ios = entry(directory, 'ios', 'directory');
  const android = entry(directory, 'android', 'directory');
  const instructionFiles = ['AGENTS.md', 'CLAUDE.md'].filter(name => entry(directory, name, 'file'));
  const dependencies = { ...(packageFile?.dependencies || {}), ...(packageFile?.devDependencies || {}) };
  const scripts = packageFile?.scripts && typeof packageFile.scripts === 'object' ? packageFile.scripts : {};
  const frameworks = [];
  if (dependencies.expo || appFile?.expo) frameworks.push('Expo');
  else if (dependencies['react-native']) frameworks.push('React Native');
  if (pubspec) frameworks.push('Flutter');
  if (dependencies.next) frameworks.push('Next.js');
  if (dependencies.vite) frameworks.push('Vite');
  const platforms = [];
  if (ios || frameworks.includes('Expo') || frameworks.includes('React Native') || pubspec) platforms.push('ios');
  if (android || frameworks.includes('Expo') || frameworks.includes('React Native') || pubspec) platforms.push('android');
  if (dependencies['react-native-web'] || dependencies.next || dependencies.vite || scripts.web) platforms.push('web');
  const availableChecks = ['lint', 'test', 'typecheck', 'check'].filter(name => Object.hasOwn(scripts, name));
  const sources = [];
  if (packageFile) sources.push('package.json');
  if (appFile) sources.push('app.json');
  if (pubspec) sources.push('pubspec.yaml');
  if (ios) sources.push('ios/');
  if (android) sources.push('android/');
  const stage = sources.length ? 'existing-app' : 'idea-or-unknown';
  const report = {
    schemaVersion: 1,
    project: path.basename(directory),
    requestedOutcome: goal,
    stage,
    platforms,
    frameworks,
    availableChecks,
    sources,
    instructionFiles,
    unknowns: stage === 'existing-app'
      ? ['Audience and success measure require user or project evidence', 'Working behavior and device status are unverified']
      : ['No supported app manifest was found', 'Audience, platforms and first useful outcome are unverified'],
    nextStep: stage === 'existing-app'
      ? 'Inspect the actual user journey and repository instructions before choosing a focused change'
      : 'Clarify the user problem and first useful result before choosing a stack',
  };
  console.log(JSON.stringify(report, null, 2));
}

try { main(); }
catch (error) { console.error(error.message); process.exitCode = 1; }
