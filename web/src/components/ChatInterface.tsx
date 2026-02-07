'use client';

import { useState, useEffect, useRef } from 'react';
import { Send, Bot, User } from 'lucide-react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

interface ChatInterfaceProps {
    postId: string;
    initialContext?: string;
    onClose?: () => void;
}

export default function ChatInterface({ postId }: ChatInterfaceProps) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [streamingContent, setStreamingContent] = useState('');
    const scrollRef = useRef<HTMLDivElement>(null);

    // Initial greeting
    useEffect(() => {
        if (messages.length === 0) {
            setMessages([{
                role: 'assistant',
                content: "Greetings. I've analyzed this intelligence report. What would you like to know about the specifics, implications, or key findings?"
            }]);
        }
    }, []);

    // Auto-scroll
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, streamingContent]);

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMsg = input;
        setInput('');
        setLoading(true);
        setStreamingContent('');

        // Add user message immediately
        const newHistory = [...messages, { role: 'user', content: userMsg } as Message];
        setMessages(newHistory);

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    postId,
                    messages: newHistory
                })
            });

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.error || "Failed to chat");
            }

            if (!res.body) throw new Error("No response body");

            // Streaming handler
            const reader = res.body.getReader();
            const decoder = new TextDecoder();
            let accumulatedText = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                accumulatedText += chunk;
                setStreamingContent(accumulatedText);
            }

            // Finalize message
            setMessages(prev => [...prev, { role: 'assistant', content: accumulatedText }]);
            setStreamingContent('');

        } catch (error: any) {
            console.error(error);
            setMessages(prev => [...prev, { role: 'assistant', content: error.message || "Sorry, I'm having trouble connecting to the intelligence network." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[600px] bg-background/50 rounded-lg border border-primary/10 overflow-hidden">
            {/* Header */}
            <div className="p-3 border-b border-primary/10 bg-primary/5 flex items-center gap-2">
                <Bot size={16} className="text-primary" />
                <span className="text-xs font-bold uppercase tracking-wider text-primary">Intelligence Assistant</span>
            </div>

            {/* Messages */}
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, idx) => (
                    <motion.div
                        key={idx}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                    >
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-cta text-white' : 'bg-primary/20 text-primary'
                            }`}>
                            {msg.role === 'user' ? <User size={14} /> : <Bot size={16} />}
                        </div>
                        <div className={`max-w-[85%] p-3 rounded-2xl text-sm leading-relaxed ${msg.role === 'user'
                            ? 'bg-cta/10 text-white rounded-tr-none border border-cta/20'
                            : 'bg-white/5 text-text/90 rounded-tl-none border border-white/10 shadow-sm'
                            }`}>
                            {msg.role === 'user' ? (
                                msg.content
                            ) : (
                                <div className="markdown-content space-y-2">
                                    <ReactMarkdown
                                        components={{
                                            ul: ({ node, ...props }) => <ul className="list-disc pl-4 space-y-1" {...props} />,
                                            ol: ({ node, ...props }) => <ol className="list-decimal pl-4 space-y-1" {...props} />,
                                            li: ({ node, ...props }) => <li className="pl-1" {...props} />,
                                            h1: ({ node, ...props }) => <h1 className="text-lg font-bold mt-2 mb-1" {...props} />,
                                            h2: ({ node, ...props }) => <h2 className="text-base font-bold mt-2 mb-1" {...props} />,
                                            h3: ({ node, ...props }) => <h3 className="text-sm font-bold mt-1" {...props} />,
                                            code: ({ node, ...props }) => <code className="bg-black/30 rounded px-1 py-0.5 font-mono text-xs" {...props} />,
                                            strong: ({ node, ...props }) => <strong className="text-primary font-bold" {...props} />
                                        }}
                                    >
                                        {msg.content}
                                    </ReactMarkdown>
                                </div>
                            )}
                        </div>
                    </motion.div>
                ))}

                {/* Streaming Message Indicator */}
                {loading && streamingContent && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex gap-3"
                    >
                        <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                            <Bot size={16} className="text-primary" />
                        </div>
                        <div className="max-w-[85%] bg-white/5 text-text/90 p-3 rounded-2xl rounded-tl-none border border-white/10 shadow-sm">
                            <div className="markdown-content space-y-2">
                                <ReactMarkdown
                                    components={{
                                        ul: ({ node, ...props }) => <ul className="list-disc pl-4 space-y-1" {...props} />,
                                        ol: ({ node, ...props }) => <ol className="list-decimal pl-4 space-y-1" {...props} />,
                                        li: ({ node, ...props }) => <li className="pl-1" {...props} />,
                                        h1: ({ node, ...props }) => <h1 className="text-lg font-bold mt-2 mb-1" {...props} />,
                                        h2: ({ node, ...props }) => <h2 className="text-base font-bold mt-2 mb-1" {...props} />,
                                        h3: ({ node, ...props }) => <h3 className="text-sm font-bold mt-1" {...props} />,
                                        code: ({ node, ...props }) => <code className="bg-black/30 rounded px-1 py-0.5 font-mono text-xs" {...props} />,
                                        strong: ({ node, ...props }) => <strong className="text-primary font-bold" {...props} />
                                    }}
                                >
                                    {streamingContent}
                                </ReactMarkdown>
                            </div>
                            <span className="inline-block w-1.5 h-4 bg-primary/50 ml-1 animate-pulse align-middle"></span>
                        </div>
                    </motion.div>
                )}

                {loading && !streamingContent && (
                    <div className="flex gap-3">
                        <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                            <Bot size={16} className="text-primary" />
                        </div>
                        <div className="bg-white/5 p-3 rounded-2xl rounded-tl-none border border-white/10 shadow-sm">
                            <div className="flex gap-1.5 p-1">
                                <span className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce"></span>
                                <span className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                                <span className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce [animation-delay:0.4s]"></span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Input */}
            <div className="p-3 border-t border-primary/10 bg-background/80 backdrop-blur">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Ask deeper questions..."
                        className="flex-1 bg-white/5 border border-primary/20 rounded-lg px-4 py-2 text-sm text-text focus:outline-none focus:border-primary/50 transition-colors placeholder:text-text/30"
                    />
                    <button
                        onClick={handleSend}
                        disabled={loading || !input.trim()}
                        className="p-2 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg active:scale-95"
                    >
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </div>
    );
}
