import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';
import { GoogleGenerativeAI } from "@google/generative-ai";

export async function POST(request: Request) {
    try {
        const { postId, messages } = await request.json();
        const userMessage = messages[messages.length - 1].content;

        if (!process.env.GOOGLE_API_KEY) {
            console.error("Missing GOOGLE_API_KEY environment variable");
            return NextResponse.json({ error: 'System Configuration Error' }, { status: 500 });
        }

        // 1. Get Context from DB
        const db = getDb();
        const dbResult = await db.execute({
            sql: 'SELECT headline, title, summary, source, status, analysis_json, facts_json FROM articles WHERE id = ?',
            args: [postId]
        });
        const post = dbResult.rows[0] as any;

        if (!post) {
            return NextResponse.json({ error: 'Intelligence Archive not found' }, { status: 404 });
        }

        const facts = typeof post.facts_json === 'string' ? JSON.parse(post.facts_json) : (post.facts_json || {});
        const analysis = typeof post.analysis_json === 'string' ? JSON.parse(post.analysis_json) : (post.analysis_json || {});

        // 2. USE GEMINI 3 PRO for deep analytical chat (Hackathon Requirement)
        const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
        // Using "gemini-3-pro-preview" for state-of-the-art reasoning
        const model = genAI.getGenerativeModel({ model: "gemini-3-pro-preview" });

        const prompt = `
            You are the LLM Lens Intelligence Assistant powered by Gemini 3. 
            Analyze the following news report and provide a high-level technical response to the user.
            
            REPORT CONTEXT:
            Headline: ${post.headline || post.title}
            Source: ${post.source}
            Summary: ${post.summary}
            Distilled Facts: ${JSON.stringify(facts)}
            AI Analysis: ${JSON.stringify(analysis)}
            
            USER QUESTION:
            ${userMessage}
            
            Gemini 3 Analysis Guidelines:
            - Provide sharp, expert insight that is accessible yet sophisticated.
            - Focus on the core 'why' and 'how' of the story.
            - Keep responses concise and high-impact; avoid long-winded technical breakdowns unless explicitly asked.
            - DO NOT use LaTeX-style math notation (e.g., avoid symbols like $, /rightarrow, or backslashes). Use plain text or standard Markdown arrows (->) instead.
            - Maintain a professional, visionary tone without being overly academic.
            - Use Markdown bolding for key terms and lists for structured data.
            - If details aren't in the report, briefly supplement with your internal knowledge.
        `;

        const result = await model.generateContentStream(prompt);

        // Create a streaming response
        const stream = new ReadableStream({
            async start(controller) {
                try {
                    for await (const chunk of result.stream) {
                        const chunkText = chunk.text();
                        controller.enqueue(new TextEncoder().encode(chunkText));
                    }
                    controller.close();
                } catch (error) {
                    controller.error(error);
                }
            },
        });

        return new NextResponse(stream, {
            headers: {
                'Content-Type': 'text/plain; charset=utf-8',
                'Transfer-Encoding': 'chunked',
            },
        });

    } catch (error: any) {
        console.error("Gemini 3 Chat Error:", error);

        // Detailed error for debugging during hackathon
        const errorMessage = error.message?.includes("404")
            ? "Gemini 3 Pro model not found. Critical hackathon dependency check failed."
            : "Failed to connect to the Gemini 3 intelligence network.";

        return NextResponse.json({ error: errorMessage }, { status: 500 });
    }
}
