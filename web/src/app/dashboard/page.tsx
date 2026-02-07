"use client";
import { useEffect, useState } from "react";
import NewsCard from "@/components/NewsCard";
import { motion } from "framer-motion";
import Link from "next/link";

interface NewsItem {
    id: string;
    title: string;
    url?: string;
    image_url?: string;
    source: string;
    full_content: string;
    facts: {
        headline: string;
        simple_explanation: string;
        key_stats: string[];
    };
    analysis: {
        category: string;
    };
}

export default function DashboardPage() {
    const [items, setItems] = useState<NewsItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [loadingMore, setLoadingMore] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const [selectedSource, setSelectedSource] = useState("All");

    const ITEMS_PER_PAGE = 30;
    const SOURCES = [
        "All",
        "TechCrunch AI",
        "VentureBeat AI",
        "MIT Tech Review AI",
        "Wired AI",
        "Guardian AI",
        "The Verge - AI",
        "r/OpenAI",
        "r/MachineLearning",
        "r/LocalLLaMA",
        "r/artificial",
    ];

    const fetchFeed = async (offset: number = 0, append: boolean = false, source: string = selectedSource) => {
        try {
            const res = await fetch(`/api/feed?offset=${offset}&limit=${ITEMS_PER_PAGE}&source=${encodeURIComponent(source)}`);
            if (res.ok) {
                const data = await res.json();

                if (data.length < ITEMS_PER_PAGE) {
                    setHasMore(false);
                } else {
                    setHasMore(true);
                }

                if (append) {
                    setItems(prev => [...prev, ...data]);
                } else {
                    setItems(data);
                }
            }
        } catch (error) {
            console.error("Failed to fetch feed", error);
        } finally {
            setLoading(false);
            setLoadingMore(false);
        }
    };

    useEffect(() => {
        setLoading(true);
        fetchFeed(0, false, selectedSource);
        const interval = setInterval(() => fetchFeed(0, false, selectedSource), 60000); // Refresh every minute
        return () => clearInterval(interval);
    }, [selectedSource]);

    const loadMore = () => {
        setLoadingMore(true);
        fetchFeed(items.length, true, selectedSource);
    };

    return (
        <div className="min-h-screen bg-background p-8">
            <div className="flex flex-col items-center mb-8">
                <h1 className="text-5xl font-black text-white mb-4 text-center text-glow tracking-tighter uppercase">
                    AI Intelligence Dashboard
                </h1>
                <div className="flex gap-4 mb-8">
                    <Link
                        href="/admin/db"
                        className="text-[10px] uppercase tracking-[0.2em] text-white/30 hover:text-blue-400 transition-colors flex items-center gap-2 border border-white/10 px-4 py-1.5 rounded-full bg-white/[0.02] hover:bg-white/[0.05]">
                        <span className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></span>
                        Database Inspector
                    </Link>
                    <span className="text-[10px] uppercase tracking-[0.2em] text-white/30 hover:text-blue-400 transition-colors flex items-center gap-2 border border-white/10 px-4 py-1.5 rounded-full bg-white/[0.02] hover:bg-white/[0.05]">
                        System Online
                    </span>
                </div>

                {/* Tag Filter Bar */}
                <div className="flex flex-wrap justify-center gap-2 max-w-4xl mx-auto px-4">
                    {SOURCES.map((source) => (
                        <button
                            key={source}
                            onClick={() => setSelectedSource(source)}
                            className={`px-4 py-2 rounded-full text-[10px] font-bold uppercase tracking-widest transition-all duration-300 border ${selectedSource === source
                                ? "bg-primary text-white border-primary shadow-[0_0_15px_rgba(0,180,255,0.4)]"
                                : "bg-white/5 text-white/40 border-white/10 hover:bg-white/10 hover:text-white"
                                }`}
                        >
                            {source}
                        </button>
                    ))}
                </div>
            </div>

            {loading ? (
                <div className="flex flex-col items-center justify-center py-24">
                    <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin mb-4"></div>
                    <div className="text-sm text-white/30 font-mono tracking-widest uppercase">Processing Archives...</div>
                </div>
            ) : items.length === 0 ? (
                <div className="text-center text-white py-24 glass-morphism rounded-3xl border border-white/10 max-w-2xl mx-auto">
                    <p className="text-xl font-medium opacity-50 italic">No items found for this source.</p>
                </div>
            ) : (
                <>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
                        {items.map((item, idx) => (
                            <motion.div
                                key={item.id || idx}
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: (idx % ITEMS_PER_PAGE) * 0.02 }}
                            >
                                <NewsCard item={item} />
                            </motion.div>
                        ))}
                    </div>

                    {hasMore && (
                        <div className="flex justify-center mt-12 pb-24">
                            <button
                                onClick={loadMore}
                                disabled={loadingMore}
                                className="px-8 py-4 bg-white/5 hover:bg-white/10 text-white text-xs tracking-widest uppercase font-bold rounded-full border border-white/10 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed hover:scale-105"
                            >
                                {loadingMore ? (
                                    <>
                                        <div className="inline-block w-3 h-3 border border-white/30 border-t-white rounded-full animate-spin mr-2"></div>
                                        Syncing...
                                    </>
                                ) : (
                                    'Load Older Archives'
                                )}
                            </button>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}
