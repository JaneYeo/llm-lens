#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Lens Marathon Loop v3.0 (Agentic Workflow)
The autonomous orchestrator for ingestion, distillation, verification, and critique.
"""
import os
import sys
import time
import subprocess
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Configuration
CYCLE_WAIT_TIME = 1800  # 30 minutes between full cycles
AGENTS_DIR = os.path.join(os.getcwd(), 'execution')

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] MARATHON: {msg}")

def run_agent(script_name):
    script_path = os.path.join(AGENTS_DIR, script_name)
    if not os.path.exists(script_path):
        log(f"Warning: {script_name} not found at {script_path}. Skipping.")
        return False
    
    log(f"-> EXECUTING: {script_name}")
    try:
        # Run and wait for completion
        result = subprocess.run([sys.executable, script_path], check=True, text=True, capture_output=True)
        # Log limited output to keep console clean
        output_lines = result.stdout.splitlines()
        for line in output_lines[-5:]: # Show last 5 lines for better debugging
            if line.strip(): print(f"   | {line.strip()}")
        log(f"-> COMPLETED: {script_name}")
        return True
    except subprocess.CalledProcessError as e:
        log(f"!! ERROR in {script_name}: {e}")
        if e.stdout: print(f"   STDOUT: {e.stdout[-300:]}")
        if e.stderr: print(f"   STDERR: {e.stderr[-300:]}")
        return False

import argparse

def main():
    parser = argparse.ArgumentParser(description="LLM Lens Autonomous Pipeline")
    parser.add_argument("--run-once", action="store_true", help="Run a single cycle and exit")
    args = parser.parse_args()

    log("=== LLM LENS AUTONOMOUS AGENTIC PIPELINE v3.0 ===")
    log("Gemini 3 Pro + Flash Full Loop Activated")
    if args.run_once:
        log("Mode: SINGLE RUN (Cloud/CI Compatible)")
    else:
        log(f"Mode: CONTINUOUS LOOP (Frequency: {CYCLE_WAIT_TIME/60} mins)")
    
    while True:
        cycle_start = time.time()
        log("--- STARTING NEW AGENTIC CYCLE ---")
        
        # 1. Ingestion: Fetch latest AI news from RSS/Reddit
        run_agent("ingest_news.py")
        
        # 2. Filtering: Identify high-value news items using Gemini scoring
        run_agent("analyze_relevance.py")
        
        # 3. Fact Distillation: Extract core insights using Gemini 3 Flash
        run_agent("distill_facts.py")
        
        # 4. Fact Verification (NEW): Audit the text facts for integrity
        run_agent("verify_facts.py")
        
        # 5. Visual Generation: Create HUD infographics using Nano Banana Pro
        run_agent("generate_ai_visuals.py")

        # 5.5. Cloud Sync (NEW): Upload to Cloudinary
        run_agent("upload_visuals.py")
        
        # 6. Self-Critique Agent (ACTIVATED): Review visuals via Gemini 3 Vision
        run_agent("self_critique.py")
        
        cycle_duration = time.time() - cycle_start
        log(f"Agentic Cycle completed in {cycle_duration/60:.2f} minutes")
        
        if args.run_once:
            log("Single run completed. Exiting.")
            break
        
        # Progress check
        wait_time = max(0, CYCLE_WAIT_TIME - cycle_duration)
        log(f"SYSTEM SLEEP: {wait_time/60:.2f} minutes until next update...")
        time.sleep(wait_time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Marathon Loop manually terminated.")
