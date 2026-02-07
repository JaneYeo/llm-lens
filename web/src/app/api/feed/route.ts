import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export async function GET(request: Request) {
    try {
        const { searchParams } = new URL(request.url);
        const offset = parseInt(searchParams.get('offset') || '0');
        const limit = parseInt(searchParams.get('limit') || '30');
        const source = searchParams.get('source');

        const db = getDb();
        let querySql = "SELECT * FROM articles WHERE status IN ('visualized', 'distilled')";
        const params: any[] = [];

        if (source && source !== 'All') {
            querySql += " AND source = ?";
            params.push(source);
        }

        querySql += " ORDER BY published DESC LIMIT ? OFFSET ?";
        params.push(limit, offset);

        const result = await db.execute({
            sql: querySql,
            args: params
        });

        const feed = result.rows.map((row: any) => {
            const facts = row.facts_json ? JSON.parse(row.facts_json) : {};
            const analysis = row.analysis_json ? JSON.parse(row.analysis_json) : {};

            return {
                id: row.id,
                title: row.headline || row.title,
                url: row.url,
                image_url: row.image_path,
                source: row.source,
                full_content: row.summary,
                facts: {
                    headline: row.headline || row.title,
                    simple_explanation: facts.simple_explanation || row.summary,
                    key_stats: facts.key_stats || []
                },
                analysis: analysis || { category: 'General' }
            };
        });

        return NextResponse.json(feed);
    } catch (error) {
        console.error("Database Error:", error);
        return NextResponse.json({ error: 'Database Feed Error' }, { status: 500 });
    }
}
