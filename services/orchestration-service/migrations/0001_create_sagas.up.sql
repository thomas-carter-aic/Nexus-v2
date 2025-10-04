CREATE TABLE IF NOT EXISTS sagas (
  id TEXT PRIMARY KEY,
  user_id TEXT,
  state TEXT,
  updated_at TIMESTAMP,
  payload JSONB
);
