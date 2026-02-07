'use client';

import { useState } from 'react';
import { Sparkles, Activity } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ChatInterface from './ChatInterface';

interface NewsCardProps {
    item: any;
}

export default function NewsCard({ item }: NewsCardProps) {
    const { title, facts, image_url, source } = item;
    const [explaining, setExplaining] = useState(false);
    const [isPreviewing, setIsPreviewing] = useState(false);

    const handleExplain = () => {
        setExplaining(!explaining);
    };

    return (
        <div className="card h-full flex flex-col group border-none">
            <div className="flex-1 p-6">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                        <div className="p-1.5 bg-primary/5 rounded border border-primary/10">
                            <Activity size={14} className="text-primary" />
                        </div>
                        <span className="text-text/50 text-xs font-mono font-medium uppercase tracking-wider">{source}</span>
                    </div>
                    {item.url && (
                        <a
                            href={item.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[10px] font-bold text-text/30 hover:text-primary transition-colors flex items-center gap-1 uppercase tracking-tighter"
                        >
                            Source Post ↗
                        </a>
                    )}
                </div>

                <h2 className="text-2xl font-heading font-bold text-text mb-6 leading-tight group-hover:text-primary transition-colors">
                    {facts?.headline || title}
                </h2>

                {image_url && (
                    <div
                        onClick={() => setIsPreviewing(true)}
                        className="block relative h-64 w-full mb-6 rounded-xl overflow-hidden border border-primary/10 cursor-zoom-in"
                    >
                        <img
                            src={image_url}
                            alt={title}
                            className="object-cover w-full h-full transform group-hover:scale-105 transition-transform duration-700"
                        />
                        <div className="absolute top-3 left-3">
                            <span className="px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-white bg-black/50 backdrop-blur-md rounded-full border border-white/10">
                                {item.analysis?.category || 'Intelligence'}
                            </span>
                        </div>
                        <div className="absolute inset-0 bg-primary/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                            <Sparkles className="text-white w-8 h-8 animate-pulse" />
                        </div>
                    </div>
                )}

                {/* Fullscreen Preview Modal */}
                <AnimatePresence>
                    {isPreviewing && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsPreviewing(false)}
                            className="fixed inset-0 z-[100] bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 md:p-8 cursor-zoom-out"
                        >
                            <motion.div
                                initial={{ scale: 0.9, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                exit={{ scale: 0.9, opacity: 0 }}
                                className="relative max-w-full max-h-full flex items-center justify-center"
                                onClick={(e) => e.stopPropagation()}
                            >
                                <img
                                    src={image_url}
                                    alt={title}
                                    className="max-w-full max-h-[90vh] object-contain rounded-lg shadow-[0_0_50px_rgba(0,0,0,0.5)] border border-white/10"
                                />
                                <button
                                    onClick={() => setIsPreviewing(false)}
                                    className="absolute -top-12 right-0 text-white/70 hover:text-white transition-colors flex items-center gap-2 text-xs font-bold tracking-widest uppercase"
                                >
                                    Close [ESC]
                                </button>
                            </motion.div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {facts?.simple_explanation && (
                    <p className="text-text/70 text-base mb-6 font-body leading-relaxed">
                        {facts.simple_explanation}
                    </p>
                )}

                {facts?.key_stats && facts.key_stats.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-auto">
                        {facts.key_stats.slice(0, 3).map((stat: string, i: number) => (
                            <span key={i} className="px-3 py-1.5 text-xs font-mono font-bold text-cta bg-cta/5 rounded-md border border-cta/10 uppercase tracking-tight">
                                {stat}
                            </span>
                        ))}
                    </div>
                )}
            </div>

            <div className="mt-6 pt-6 border-t border-primary/5 space-y-3">
                <button
                    onClick={handleExplain}
                    className="w-full px-4 py-2.5 text-xs font-bold text-white bg-cta rounded-lg hover:bg-blue-700 transition-all duration-300 shadow-md group/btn flex items-center justify-center gap-2"
                >
                    {explaining ? (
                        <>
                            Close Intelligence
                        </>
                    ) : (
                        <>
                            <Sparkles size={14} className="group-hover:rotate-12 transition-transform" />
                            I want to know more
                        </>
                    )}
                </button>

                <AnimatePresence>
                    {explaining && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="overflow-hidden"
                        >
                            <ChatInterface
                                postId={item.id}
                                initialContext={item.full_content || item.facts?.simple_explanation}
                            />
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
