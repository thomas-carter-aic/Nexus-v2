import { Pool } from 'pg';
export const createDbPool = () => new Pool({ connectionString: 'postgres://user:pass@localhost:5432/db' });
