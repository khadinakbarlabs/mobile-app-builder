// Publisher-only native discovery; this does not start a model session or run an Actor.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

try {
  if (!process.argv[2]) throw new Error('Pass an installed plugin root');
  const root = path.resolve(process.argv[2]);
  const manifest = JSON.parse(fs.readFileSync(path.join(root, '.claude-plugin/plugin.json'), 'utf8'));
  const expected = {
    skills: fs.readdirSync(path.join(root, 'skills')).filter(name => fs.existsSync(path.join(root, 'skills', name, 'SKILL.md'))).sort(),
    agents: fs.existsSync(path.join(root, 'agents')) ? fs.readdirSync(path.join(root, 'agents')).filter(name => name.endsWith('.md')).map(name => name.slice(0, -3)).sort() : [],
  };
  const output = execFileSync('npx', ['--yes', '@anthropic-ai/claude-code@2.1.287', '--plugin-dir', root, 'plugin', 'details', `${manifest.name}@inline`], { encoding: 'utf8', timeout: 60000, maxBuffer: 2 * 1024 * 1024 });
  const actual = {};
  for (const kind of ['skills', 'agents']) {
    const label = kind[0].toUpperCase() + kind.slice(1);
    const match = output.match(new RegExp(`^\\s*${label} \\((\\d+)\\)[ \\t]*(.*)$`, 'm'));
    if (!match) {
      if (!expected[kind].length && !output.includes(label + ' (')) { actual[kind] = []; continue; }
      throw new Error(`Missing native ${kind} inventory`);
    }
    const names = match[2].trim() ? match[2].trim().split(/,\s*/).sort() : [];
    if (Number(match[1]) !== names.length || JSON.stringify(names) !== JSON.stringify(expected[kind])) throw new Error(`Native ${kind} inventory differs from installed components`);
    actual[kind] = names;
  }
  console.log(JSON.stringify({ name: manifest.name, version: manifest.version, claudeVersion: '2.1.287', status: 'host-discovery-passed', actual, liveActorRunVerified: false, directoryApproval: false }, null, 2));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
