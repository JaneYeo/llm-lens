'use client';

import { useEffect, useRef } from 'react';
import Link from 'next/link';
import * as THREE from 'three';
import { motion, useScroll, useSpring, useTransform } from 'framer-motion';
import { ArrowLeft, Cpu, Database, Eye, Layers, Zap, CheckCircle2 } from 'lucide-react';

export default function TechnicalDeck() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);
    const sceneRef = useRef<THREE.Scene>(null);
    const cameraRef = useRef<THREE.PerspectiveCamera>(null);
    const groupRef = useRef<THREE.Group>(null);

    const { scrollYProgress } = useScroll({
        target: containerRef,
        offset: ["start start", "end end"]
    });

    const smoothProgress = useSpring(scrollYProgress, { stiffness: 100, damping: 30 });

    // Correctly map scroll progress to 3D pipeline positions
    // Total vertical travel for 6 stages (y=12 to y=-8) is exactly 20 units.
    // Progress 0 is Step 1, Progress 0.833 is Step 6 (5 intervals of 1/6 each)
    const groupY = useTransform(smoothProgress, [0, 0.833], [-12, 8]);

    // Fade out labels and 3D when we head towards the footer
    const sceneOpacity = useTransform(smoothProgress, [0.833, 1], [1, 0]);

    useEffect(() => {
        if (!canvasRef.current) return;

        const scene = new THREE.Scene();
        sceneRef.current = scene;
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        cameraRef.current = camera;
        const renderer = new THREE.WebGLRenderer({
            canvas: canvasRef.current,
            alpha: true,
            antialias: true
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);

        const group = new THREE.Group();
        groupRef.current = group;
        scene.add(group);

        // --- PIPELINE OBJECTS ---
        const stages: THREE.Group[] = [];

        // 1. Data Ingestion (Floating shards)
        const stage1 = new THREE.Group();
        for (let i = 0; i < 30; i++) {
            const mesh = new THREE.Mesh(
                new THREE.BoxGeometry(0.1, 0.1, 0.1),
                new THREE.MeshStandardMaterial({ color: 0x3b82f6, emissive: 0x3b82f6, emissiveIntensity: 0.5 })
            );
            mesh.position.set((Math.random() - 0.5) * 4, (Math.random() - 0.5) * 4, (Math.random() - 0.5) * 4);
            stage1.add(mesh);
        }
        stage1.position.y = 12;
        group.add(stage1);
        stages.push(stage1);

        // 2. Scoring Filter (Scanning Ring)
        const stage2 = new THREE.Group();
        const torus = new THREE.Mesh(
            new THREE.TorusGeometry(1.5, 0.05, 16, 100),
            new THREE.MeshStandardMaterial({ color: 0xfacc15, emissive: 0xfacc15, emissiveIntensity: 1 })
        );
        stage2.add(torus);
        stage2.position.y = 8;
        group.add(stage2);
        stages.push(stage2);

        // 3. Distillation Core (Complex poly)
        const stage3 = new THREE.Group();
        const dodeca = new THREE.Mesh(
            new THREE.DodecahedronGeometry(1.2, 0),
            new THREE.MeshStandardMaterial({ color: 0xc084fc, wireframe: true, emissive: 0xc084fc, emissiveIntensity: 1.5 })
        );
        stage3.add(dodeca);
        stage3.position.y = 4;
        group.add(stage3);
        stages.push(stage3);

        // 4. Verification Gate (Hexagon grid)
        const stage4 = new THREE.Group();
        const hex = new THREE.Mesh(
            new THREE.IcosahedronGeometry(1.5, 1),
            new THREE.MeshStandardMaterial({ color: 0x4ade80, wireframe: true, transparent: true, opacity: 0.6, emissive: 0x4ade80, emissiveIntensity: 1.5 })
        );
        stage4.add(hex);
        stage4.position.y = 0;
        group.add(stage4);
        stages.push(stage4);

        // 5. Visual Synthesis (Hologram stack)
        const stage5 = new THREE.Group();
        for (let i = 0; i < 5; i++) {
            const plane = new THREE.Mesh(
                new THREE.PlaneGeometry(2, 0.1),
                new THREE.MeshBasicMaterial({ color: 0xf97316, transparent: true, opacity: 0.5, side: THREE.DoubleSide })
            );
            plane.position.y = (i - 2) * 0.4;
            stage5.add(plane);
        }
        stage5.position.y = -4;
        group.add(stage5);
        stages.push(stage5);

        // 6. Critique (Scanning Eye)
        const stage6 = new THREE.Group();
        const ring = new THREE.Mesh(
            new THREE.RingGeometry(0.8, 1, 32),
            new THREE.MeshBasicMaterial({ color: 0x3b82f6, side: THREE.DoubleSide })
        );
        const center = new THREE.Mesh(
            new THREE.SphereGeometry(0.2, 16, 16),
            new THREE.MeshBasicMaterial({ color: 0xffffff })
        );
        stage6.add(ring, center);
        stage6.position.y = -8;
        group.add(stage6);
        stages.push(stage6);

        // Lights
        const pointLight = new THREE.PointLight(0xffffff, 20, 50);
        pointLight.position.set(5, 5, 5);
        scene.add(pointLight);
        scene.add(new THREE.AmbientLight(0x404040));

        camera.position.z = 8;

        const animate = () => {
            requestAnimationFrame(animate);
            if (groupRef.current) {
                groupRef.current.position.y = groupY.get();
            }

            // Local animations
            stage1.rotation.y += 0.005;
            stage2.rotation.x += 0.02;
            stage3.rotation.y -= 0.01;
            stage4.rotation.z += 0.005;
            stage5.children.forEach((p, i) => {
                p.rotation.y += 0.01 * (i + 1);
            });
            stage6.rotation.z += 0.05;

            renderer.render(scene, camera);
        };
        animate();

        const handleResize = () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        };
        window.addEventListener('resize', handleResize);

        return () => window.removeEventListener('resize', handleResize);
    }, [groupY]);

    const steps = [
        { id: 1, title: 'Autonomous Ingestion', desc: 'Harvesting raw data from premium sources (Wired, TechCrunch).', icon: Database, color: 'text-blue-400' },
        { id: 2, title: 'Relevance Scoring', desc: 'Gemini 3 Pro evaluates importance vs noise.', icon: Zap, color: 'text-yellow-400' },
        { id: 3, title: 'Fact Distillation', desc: 'Extracting key metrics and core headlines.', icon: Cpu, color: 'text-purple-400' },
        { id: 4, title: 'Fact Verification', desc: 'Audit checking claims for data integrity.', icon: CheckCircle2, color: 'text-green-400' },
        { id: 5, title: 'Visual Synthesis', desc: 'Nano Banana Pro renders high-res infographics.', icon: Layers, color: 'text-cta' },
        { id: 6, title: 'Model Critique', desc: 'Vision agents cross-verify output fidelity.', icon: Eye, color: 'text-blue-500' }
    ];

    return (
        <main ref={containerRef} className="min-h-[700vh] bg-[#02020a] text-text relative">
            <motion.canvas
                ref={canvasRef}
                style={{ opacity: sceneOpacity }}
                className="fixed inset-0 z-0 pointer-events-none"
            />

            <nav className="fixed top-0 left-0 p-8 z-50">
                <Link href="/" className="flex items-center gap-2 group text-text/60 hover:text-white transition-colors">
                    <ArrowLeft size={20} className="group-hover:-translate-x-1 transition-transform" />
                    <span className="font-heading font-bold text-sm uppercase tracking-widest">Exit Technical Deck</span>
                </Link>
            </nav>

            {/* Sticky Title */}
            <motion.div
                style={{
                    opacity: useTransform(smoothProgress, [0, 0.8, 0.9], [1, 1, 0]),
                    pointerEvents: useTransform(smoothProgress, [0, 0.8, 0.9], ["auto", "auto", "none"])
                }}
                className="fixed top-32 left-8 md:left-24 z-20 pointer-events-none max-w-[250px] md:max-w-none"
            >
                <h1 className="text-3xl md:text-6xl font-heading font-black text-white leading-tight tracking-tighter">
                    ENGINEERING <br /> <span className="text-primary">PROCESS.</span>
                </h1>
                <div className="mt-8 flex items-center gap-6">
                    <div className="w-1.5 h-32 md:h-48 bg-white/5 relative rounded-full overflow-hidden">
                        <motion.div
                            style={{ height: useTransform(smoothProgress, [0, 1], ["0%", "100%"]) }}
                            className="absolute top-0 left-0 w-full bg-primary shadow-[0_0_20px_#3b82f6]"
                        />
                    </div>
                    <div className="hidden md:flex flex-col gap-4 text-[10px] uppercase tracking-[0.4em] text-white/30 font-bold">
                        {steps.map(s => (
                            <motion.span
                                key={s.id}
                                style={{
                                    opacity: useTransform(
                                        smoothProgress,
                                        [(s.id - 2) / 6, (s.id - 1) / 6, s.id / 6],
                                        [0.2, 1, 0.2]
                                    ),
                                    color: useTransform(
                                        smoothProgress,
                                        [(s.id - 2) / 6, (s.id - 1) / 6, s.id / 6],
                                        ["rgba(255,255,255,0.3)", "rgba(59,130,246,1)", "rgba(255,255,255,0.3)"]
                                    )
                                }}
                            >
                                Step 0{s.id}
                            </motion.span>
                        ))}
                    </div>
                </div>
            </motion.div>

            <div className="max-w-7xl mx-auto px-6 relative z-10">
                {steps.map((step) => (
                    <section key={step.id} className="h-screen flex items-center justify-end">
                        <motion.div
                            initial={{ opacity: 0, x: 100 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            transition={{ type: "spring", damping: 20 }}
                            viewport={{ margin: "-20%" }}
                            className="w-full md:w-5/12 glass-card p-10 md:p-14 relative group border-white/5 hover:border-primary/20 transition-colors"
                        >
                            <div className="absolute -left-6 top-1/2 -translate-y-1/2 w-12 h-12 bg-black border border-white/10 rounded-full flex items-center justify-center text-primary font-mono font-bold text-xl shadow-2xl backdrop-blur-xl group-hover:border-primary/40 transition-colors">
                                {step.id}
                            </div>

                            <div className={`w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center mb-8 ${step.color} shadow-inner`}>
                                <step.icon size={40} />
                            </div>

                            <h2 className="text-4xl font-heading font-black text-white mb-6 uppercase tracking-tighter">
                                {step.title}
                            </h2>

                            <p className="text-xl text-text/50 font-body leading-relaxed">
                                {step.desc}
                            </p>
                        </motion.div>
                    </section>
                ))}
            </div>

            {/* Terminal State Footer */}
            <section className="h-screen flex items-center justify-center relative">
                <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    className="glass-card p-16 max-w-3xl text-center border-primary/20 bg-primary/5 relative z-10 overflow-hidden"
                >
                    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-primary to-transparent opacity-50" />

                    <h2 className="text-5xl font-heading font-black text-white mb-8 uppercase tracking-tighter text-glow">
                        INTEGRATION COMPLETE.
                    </h2>

                    <p className="text-xl text-text/60 mb-12 font-body max-w-xl mx-auto">
                        The LLM Lens engine is now synchronized. Autonomous agents are standing by for next-generation intelligence delivery.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link href="/dashboard" className="btn-primary px-12 py-5 text-sm uppercase tracking-[0.3em] font-black">
                            Enter Dashboard
                        </Link>
                        <Link href="/" className="btn-secondary px-12 py-5 text-sm uppercase tracking-[0.3em] font-black">
                            Main Menu
                        </Link>
                    </div>
                </motion.div>
            </section>
        </main>
    );
}
