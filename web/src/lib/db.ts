import { createClient } from '@libsql/client';

const url = process.env.TURSO_DATABASE_URL || "file:../llm_lens.db";
const authToken = process.env.TURSO_AUTH_TOKEN;

/**
 * Turso/LibSQL client for authenticated cloud access OR local SQLite.
 */
export const db = createClient({
    url: url,
    authToken: authToken,
});

/**
 * Legacy getter - note that this now returns an ASYNC-capable client.
 * All DB operations in API routes must be AWAITed.
 */
export function getDb() {
    return db;
}
