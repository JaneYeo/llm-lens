import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export async function GET() {
    try {
        const db = getDb();
        const result = await db.execute('SELECT * FROM articles ORDER BY created_at DESC');

        return NextResponse.json(result.rows);
    } catch (error) {
        console.error("Database Inspector API Error:", error);
        return NextResponse.json({ error: 'Failed to fetch database content' }, { status: 500 });
    }
}
