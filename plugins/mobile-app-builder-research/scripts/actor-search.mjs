#!/usr/bin/env node

// Search public Actor listings through the installed CLI without opening its saved login.
import { execFile } from 'node:child_process';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { promisify } from 'node:util';

const run = promisify(execFile);

function options(args) {
  if (args.length !== 4 || args[0] !== '--query' || args[2] !== '--limit') {
    throw new Error('Usage: node scripts/actor-search.mjs --query "topic" --limit 1-20');
  }
  const query = args[1].trim();
  const limit = Number(args[3]);
  if (!query || query.length > 200 || query.startsWith('-') || /[\x00-\x1f\x7f]/.test(query)) {
    throw new Error('Provide a plain search topic of at most 200 characters.');
  }
  if (!Number.isInteger(limit) || limit < 1 || limit > 20) {
    throw new Error('Limit must be an integer from 1 to 20.');
  }
  return { query, limit };
}

async function main() {
  const { query, limit } = options(process.argv.slice(2));
  const temporaryHome = await mkdtemp(join(tmpdir(), 'mobile-research-'));
  try {
    const { stdout } = await run('apify', ['actors', 'search', query, '--json', '--limit', String(limit)], {
      cwd: temporaryHome,
      env: {
        PATH: process.env.PATH || '',
        HOME: temporaryHome,
        XDG_CONFIG_HOME: temporaryHome,
        APIFY_CLI_SKIP_UPDATE_CHECK: '1',
        APIFY_CLI_DISABLE_TELEMETRY: '1',
      },
      timeout: 25000,
      maxBuffer: 256 * 1024,
      shell: false,
    });
    const result = JSON.parse(stdout);
    if (!Array.isArray(result.items)) throw new Error('Unexpected CLI response');
    const actors = result.items.slice(0, limit).map((item) => ({
      id: `${item.username}/${item.name}`,
      title: String(item.title || '').slice(0, 160),
      description: String(item.description || '').slice(0, 400),
    }));
    process.stdout.write(`${JSON.stringify({ query, actors, note: 'Discovery only; inspect the current schema, pricing and rights before any run.' }, null, 2)}\n`);
  } finally {
    await rm(temporaryHome, { recursive: true, force: true });
  }
}

main().catch((error) => {
  const message = error.code === 'ENOENT'
    ? 'Apify CLI is unavailable. Install it from the official CLI documentation before using this optional command.'
    : error.message.startsWith('Usage:') || error.message.startsWith('Provide a plain') || error.message.startsWith('Limit must')
      ? error.message
      : 'Actor discovery failed. Check the CLI installation and try again.';
  process.stderr.write(`${message}\n`);
  process.exitCode = 1;
});
