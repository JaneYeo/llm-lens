'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowRight, BarChart3, Globe2, ShieldCheck, Zap, Newspaper, Box } from 'lucide-react';

export default function Home() {
  return (
    <main className="min-h-screen bg-background selection:bg-primary/20 text-text">
      {/* Floating Navbar */}
      <nav className="fixed top-4 left-4 right-4 z-50">
        <div className="max-w-7xl mx-auto glass-card px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 group cursor-pointer">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white font-bold shadow-[0_0_15px_rgba(59,130,246,0.5)] group-hover:rotate-12 transition-transform">
              L
            </div>
            <span className="font-heading font-bold text-xl text-primary tracking-tighter text-glow">
              LLM LENS
            </span>
          </div>
          <div className="hidden md:flex items-center space-x-8 text-sm font-medium text-text/70">
            <a href="#features" className="hover:text-primary transition-colors cursor-pointer">Features</a>
            <a href="#social-proof" className="hover:text-primary transition-colors cursor-pointer">Testimonials</a>
            <Link href="/dashboard" className="btn-primary py-2 px-5 text-sm uppercase tracking-wider">
              Dashboard
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section - 3D Perspective */}
      <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden">
        {/* Galaxy Gradient Background */}
        <div className="absolute inset-x-0 top-0 h-[1000px] -z-10 overflow-hidden">
          <div className="absolute top-[-10%] left-[-10%] w-[120%] h-[120%] bg-[radial-gradient(circle_at_center,rgba(59,130,246,0.1)_0%,transparent_70%)] opacity-50 blur-3xl animate-pulse"></div>
          <div className="absolute bottom-0 left-0 right-0 h-64 bg-gradient-to-t from-background to-transparent"></div>
        </div>

        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="text-left"
          >
            <span className="inline-block px-4 py-1.5 bg-primary/10 text-primary text-[10px] font-bold rounded-full mb-6 border border-primary/30 uppercase tracking-[0.3em] backdrop-blur-sm">
              AI-Powered News Intelligence
            </span>
            <h1 className="text-6xl md:text-8xl font-heading font-black text-white mb-8 leading-[1] tracking-tighter text-glow">
              AI TRENDS, <br />
              <span className="text-cta">VISUALIZED.</span>
            </h1>
            <p className="text-lg md:text-xl text-text/60 max-w-xl mb-10 leading-relaxed font-body">
              The world's first autonomous AI news hub. We aggregate, verify, and distill the latest breakthroughs into high-impact visuals.
            </p>
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <Link href="/dashboard" className="btn-primary flex items-center gap-2 group text-sm px-8 uppercase tracking-widest">
                Explore Feed
                <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link href="/technical-deck" className="btn-secondary text-sm px-8 uppercase tracking-widest">
                Technical Deck
              </Link>
            </div>
          </motion.div>

          {/* 3D Animation Component: The Fact Orb */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8, rotateY: 45 }}
            animate={{ opacity: 1, scale: 1, rotateY: 0 }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            className="relative h-[400px] md:h-[500px] flex items-center justify-center perspective-[1000px]"
          >
            {/* Outer Ring 1 */}
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="absolute w-80 h-80 border-2 border-primary/20 rounded-full border-dashed"
            />
            {/* Outer Ring 2 */}
            <motion.div
              animate={{ rotate: -360 }}
              transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
              className="absolute w-64 h-64 border-2 border-cta/20 rounded-full border-dotted"
            />
            {/* The Orb */}
            <motion.div
              animate={{
                y: [0, -20, 0],
                rotateX: [0, 10, 0],
                rotateY: [0, 360]
              }}
              transition={{
                y: { duration: 4, repeat: Infinity, ease: "easeInOut" },
                rotateY: { duration: 10, repeat: Infinity, ease: "linear" }
              }}
              className="relative w-48 h-48 rounded-full bg-gradient-to-br from-primary via-blue-900 to-black shadow-[0_0_80px_rgba(59,130,246,0.6)] border border-white/20 flex items-center justify-center overflow-hidden"
              style={{ transformStyle: 'preserve-3d' }}
            >
              <Box size={80} className="text-white opacity-40" />
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,rgba(255,255,255,0.2)_0%,transparent_50%)]"></div>
              {/* Internal Glow */}
              <div className="absolute w-full h-full animate-pulse bg-primary/20 blur-xl"></div>
            </motion.div>

            {/* Floating Data Nodes */}
            {[0, 1, 2, 3].map((i) => (
              <motion.div
                key={i}
                animate={{
                  y: [0, -40, 0],
                  x: [0, (i % 2 === 0 ? 30 : -30), 0],
                  opacity: [0.3, 1, 0.3]
                }}
                transition={{
                  duration: 3 + i,
                  repeat: Infinity,
                  delay: i * 0.5
                }}
                className={`absolute w-3 h-3 rounded-full bg-primary shadow-[0_0_10px_#3B82F6]`}
                style={{
                  top: `${20 + i * 20}%`,
                  left: `${10 + i * 25}%`
                }}
              />
            ))}
          </motion.div>
        </div>

        {/* Social Proof Bar */}
        <div className="max-w-7xl mx-auto px-6 mt-24">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8, duration: 1 }}
            className="border-t border-white/5 pt-12 text-center"
          >
            <p className="text-[10px] font-bold text-text/30 uppercase tracking-[0.4em] mb-8">Aligned with Stellar Intelligence</p>
            <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-30 grayscale hover:grayscale-0 transition-all duration-500">
              <div className="font-heading font-black text-2xl tracking-tighter">NOVA-X</div>
              <div className="font-heading font-black text-2xl tracking-tighter">ASTRA</div>
              <div className="font-heading font-black text-2xl tracking-tighter">QUASAR</div>
              <div className="font-heading font-black text-2xl tracking-tighter">VOYAGER</div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section - Bento Grid style */}
      <section id="features" className="py-24 relative">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-left mb-16">
            <h2 className="text-4xl md:text-5xl font-heading font-black mb-4 text-glow">HOW IT WORKS</h2>
            <div className="h-1 w-20 bg-cta"></div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <motion.div
              whileHover={{ y: -5 }}
              className="md:col-span-2 card flex flex-col justify-between min-h-[300px]"
            >
              <div>
                <div className="w-12 h-12 bg-primary/20 rounded-xl flex items-center justify-center mb-6 text-primary shadow-[0_0_15px_rgba(59,130,246,0.3)]">
                  <Globe2 size={24} />
                </div>
                <h3 className="text-2xl font-heading font-bold mb-4">Smart Aggregation</h3>
                <p className="text-text/50 leading-relaxed font-body">Continuously monitoring premium sources like Wired, TechCrunch, The Guardian, and Reddit for breaking AI news.</p>
              </div>
              <div className="mt-8 pt-8 border-t border-white/5 flex items-center justify-between text-xs font-bold uppercase tracking-widest text-primary">
                View Sources <ArrowRight size={14} />
              </div>
            </motion.div>

            {[
              { title: 'Fact Verification', desc: 'Gemini 3 verified insights ensure 99.9% data integrity.', icon: ShieldCheck, color: 'text-cta' },
              { title: 'Visual Distillation', desc: 'Auto-generated HUD infographics for rapid consumption.', icon: BarChart3, color: 'text-blue-400' },
            ].map((feature, idx) => (
              <motion.div
                key={feature.title}
                whileHover={{ y: -5 }}
                className="card flex flex-col"
              >
                <div className={`w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center mb-6 ${feature.color}`}>
                  <feature.icon size={24} />
                </div>
                <h3 className="text-xl font-heading font-bold mb-3">{feature.title}</h3>
                <p className="text-text/50 text-sm leading-relaxed font-body">{feature.desc}</p>
              </motion.div>
            ))}

            <motion.div
              whileHover={{ y: -5 }}
              className="card bg-gradient-to-br from-cta to-orange-700 border-none flex flex-col items-center justify-center text-center group"
            >
              <Zap size={48} className="text-white mb-6 group-hover:scale-110 transition-transform" />
              <h3 className="text-xl font-heading font-bold text-white mb-2 uppercase tracking-tighter">Real-time Stream</h3>
              <p className="text-white/80 text-sm font-body">Interactive AI chat and live updates on every news item.</p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Social Proof / Testimonials */}
      <section id="social-proof" className="py-24">
        <div className="max-w-7xl mx-auto px-6">
          <div className="glass-card p-12 relative overflow-hidden group">
            <div className="absolute -right-20 -bottom-20 w-64 h-64 bg-primary/10 rounded-full blur-[100px] group-hover:bg-primary/20 transition-colors"></div>
            <div className="max-w-3xl relative z-10">
              <h2 className="text-3xl font-heading font-bold mb-8 leading-tight">"LLM LENS HAS TRANSFORMED HOW WE TRACK AI BREAKTHROUGHS. THE VISUALS ARE CRYSTAL CLEAR."</h2>
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-gradient-to-tr from-primary to-cta rounded-full shadow-[0_0_20px_rgba(59,130,246,0.5)]"></div>
                <div>
                  <p className="font-heading font-bold text-white tracking-widest text-sm uppercase">AI Engineering Lead</p>
                  <p className="text-xs text-text/40 font-body uppercase tracking-[0.2em]">Scale AI • Intelligence Ops</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-white/5">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-white/10 rounded flex items-center justify-center text-white font-bold text-[10px]">
              L
            </div>
            <span className="font-heading font-bold text-xs tracking-[0.3em] text-white">
              LLM LENS
            </span>
          </div>
          <p className="text-text/30 text-[10px] font-mono tracking-widest uppercase">© 2026 LLM LENS. ALL RIGHTS RESERVED.</p>
          <div className="flex gap-8 text-text/40 text-[10px] font-bold uppercase tracking-widest">
            {/* Links removed as they did not navigate to other pages */}
          </div>
        </div>
      </footer>
    </main>
  );
}
