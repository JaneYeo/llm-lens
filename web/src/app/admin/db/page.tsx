'use client';

import { useEffect, useState } from 'react';
import { LayoutDashboard, Database as DbIcon, RefreshCw, AlertCircle, CheckCircle2, FlaskConical, ImageIcon, Filter } from 'lucide-react';
import Link from 'next/link';

export default function DatabaseInspector() {
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = async () => {
        setLoading(true);
        try {
            const res = await fetch('/api/admin/db');
            if (!res.ok) throw new Error('Failed to fetch DB data');
            const json = await res.json();
            setData(json);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'visualized': return <ImageIcon className="w-4 h-4 text-green-400" />;
            case 'distilled': return <CheckCircle2 className="w-4 h-4 text-blue-400" />;
            case 'ingested': return <RefreshCw className="w-4 h-4 text-yellow-400" />;
            case 'filtered': return <Filter className="w-4 h-4 text-gray-500" />;
            default: return <AlertCircle className="w-4 h-4 text-red-400" />;
        }
    };

    return (
        <div className="min-h-screen bg-[#050510] text-gray-100 p-8 font-sans">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-primary/10 rounded-2xl border border-primary/20">
                            <DbIcon className="w-8 h-8 text-primary" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-500">
                                Database Inspector
                            </h1>
                            <p className="text-gray-400 text-sm">Real-time view of the LLM Lens Article pipeline</p>
                        </div>
                    </div>
                    <div className="flex gap-4">
                        <button
                            onClick={fetchData}
                            className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl border border-white/10 transition-all"
                        >
                            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                            Refresh
                        </button>
                        <Link
                            href="/dashboard"
                            className="flex items-center gap-2 px-4 py-2 bg-primary/20 hover:bg-primary/30 text-primary border border-primary/30 rounded-xl transition-all"
                        >
                            <LayoutDashboard className="w-4 h-4" />
                            Back to Dashboard
                        </Link>
                    </div>
                </div>

                {/* Status Filter Cards */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    {['ingested', 'filtered', 'distilled', 'visualized'].map(status => (
                        <div key={status} className="bg-white/5 border border-white/10 p-4 rounded-3xl flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                {getStatusIcon(status)}
                                <span className="text-xs font-bold uppercase tracking-widest text-gray-400">{status}</span>
                            </div>
                            <span className="text-xl font-mono font-bold text-white">
                                {data.filter(i => i.status === status).length}
                            </span>
                        </div>
                    ))}
                </div>

                {/* Table */}
                <div className="glass-morphism rounded-3xl overflow-hidden border border-white/10 shadow-2xl">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead>
                                <tr className="bg-white/5 border-b border-white/10">
                                    <th className="px-6 py-4 text-sm font-semibold text-gray-400">Status</th>
                                    <th className="px-6 py-4 text-sm font-semibold text-gray-400">Headline / Title</th>
                                    <th className="px-6 py-4 text-sm font-semibold text-gray-400">Source</th>
                                    <th className="px-6 py-4 text-sm font-semibold text-gray-400">Visual Path</th>
                                    <th className="px-6 py-4 text-sm font-semibold text-gray-400">Timestamp</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {loading && (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-24 text-center text-gray-500">
                                            <div className="relative w-16 h-16 mx-auto mb-4">
                                                <div className="absolute inset-0 rounded-full border-2 border-primary/20 animate-ping"></div>
                                                <RefreshCw className="w-16 h-16 text-primary animate-spin" />
                                            </div>
                                            <p className="font-mono text-sm">SCANNING NEURAL DATABASE...</p>
                                        </td>
                                    </tr>
                                )}
                                {!loading && data.length === 0 && (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-12 text-center text-gray-500 italic">
                                            No records found in the database articles table.
                                        </td>
                                    </tr>
                                )}
                                {data.map((row) => (
                                    <tr key={row.id} className="hover:bg-white/[0.03] transition-colors group">
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-2">
                                                {getStatusIcon(row.status)}
                                                <span className="text-[10px] font-mono uppercase tracking-widest font-bold">
                                                    {row.status}
                                                </span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="max-w-md">
                                                <div className="text-sm font-medium text-white truncate group-hover:text-primary transition-colors">
                                                    {row.headline || row.title}
                                                </div>
                                                <div className="text-[10px] text-gray-500 font-mono mt-1 opacity-50">
                                                    {row.id}
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className="px-2 py-0.5 bg-white/5 rounded-full text-[9px] text-gray-400 border border-white/10 uppercase font-black">
                                                {row.source}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            {row.image_path ? (
                                                <div className="text-[10px] font-mono text-primary/70 truncate max-w-[150px] bg-primary/5 px-2 py-1 rounded border border-primary/10">
                                                    {row.image_path}
                                                </div>
                                            ) : (
                                                <span className="text-[10px] text-gray-600 font-mono italic opacity-30">NOT_GENERATED</span>
                                            )}
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="text-[10px] font-mono text-gray-500 whitespace-nowrap">
                                                {new Date(row.updated_at || row.created_at).toLocaleString()}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Statistics Footer */}
                <div className="mt-6 flex items-center justify-between px-6 text-[10px] font-mono text-gray-600 uppercase tracking-widest">
                    <div>System ID: LLM-LENS-CORE-v2</div>
                    <div>Total Records: {data.length}</div>
                    <div>Active Model: Gemini-3-Pro-Preview</div>
                </div>
            </div>

            <style jsx>{`
                .glass-morphism {
                    background: rgba(10, 10, 20, 0.4);
                    backdrop-filter: blur(40px);
                    -webkit-backdrop-filter: blur(40px);
                }
            `}</style>
        </div>
    );
}
