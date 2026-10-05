export async function login(state, authenticate) {
  state.loading = true;
  state.error = null;
  const result = await authenticate();
  state.loading = false;
  return result;
}
