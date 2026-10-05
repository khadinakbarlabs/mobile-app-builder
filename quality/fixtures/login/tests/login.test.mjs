import test from 'node:test';
import assert from 'node:assert/strict';
import { login } from '../src/login.mjs';
test('rejected login stops loading and surfaces an error', async () => {
  const state = { loading: false, error: null };
  try { await login(state, async () => { throw new Error('Login unavailable'); }); } catch {}
  assert.equal(state.loading, false);
  assert.ok(state.error, 'user can see the failure');
});
test('successful login keeps its return value', async () => {
  const state = { loading: false, error: null };
  assert.equal(await login(state, async () => 'signed-in'), 'signed-in');
  assert.equal(state.loading, false);
  assert.equal(state.error, null);
});
