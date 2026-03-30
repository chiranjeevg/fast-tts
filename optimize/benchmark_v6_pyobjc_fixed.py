#!/usr/bin/env python3
"""
TTS Benchmark v6 - Fixed PyObjC AVFoundation

Uses correct PyObjC API for AVSpeechSynthesizer
"""

import os
import sys
import json
import time
from pathlib import Path

try:
    from AppKit import NSSpeechSynthesizer, NSVoice
    from Foundation import NSURL
    PYOBJC_AVAILABLE = True
except ImportError as e:
    print(f"PyObjC import error: {e}")
    PYOBJC_AVAILABLE = False


def benchmark_pyobjc_direct(text):
    """Direct PyObjC AVSpeechSynthesizer"""
    output_file = Path("/tmp/pyobjc_direct.m4a")
    
    if not PYOBJC_AVAILABLE:
        return {"elapsed_ms": 9999, "error": "PyObjC not available"}
    
    start = time.time()
    
    try:
        # Create synthesizer
        synth = NSSpeechSynthesizer.alloc().init()
        
        # Set voice by name (Alex is pre-installed on macOS)
        voices = NSVoice.speechVoices()
        alex_voice = None
        for voice in voices:
            if "Alex" in voice.name():
                alex_voice = voice
                break
        
        if alex_voice:
            synth.setVoice_(alex_voice)
        
        # Set rate (normal is ~0.5 for Alex)
        synth.setRate_(0.5)
        
        # Set volume
        synth.setVolume_(1.0)
        
        # Start speaking to file
        output_url = NSURL.fileURLWithPath_(str(output_file))
        
        # speakString_ writes to file when URL is set
        result = synth.startSpeakingString_toUrl_(text, output_url)
        
        # Wait for completion
        max_wait = 10
        elapsed = 0
        while synth.isSpeaking() and elapsed < max_wait:
            time.sleep(0.1)
            elapsed += 0.1
        
        total_elapsed = time.time() - start
        
        if output_file.exists():
            audio_size = output_file.stat().st_size
        else:
            audio_size = 0
        
        return {
            "elapsed_ms": int(total_elapsed * 1000),
            "audio_size_bytes": audio_size,
            "success": output_file.exists(),
            "method": "PyObjC AVSpeechSynthesizer"
        }
    
    except Exception as e:
        elapsed = time.time() - start
        return {
            "elapsed_ms": int(elapsed * 1000),
            "error": str(e),
            "success": False,
            "method": "PyObjC (error)"
        }


def benchmark_applescript_baseline(text):
    """AppleScript baseline"""
    output_file = Path("/tmp/applescript_baseline.aiff")
    
    script = f'''
set outputFile to POSIX path of "{output_file}"
do shell script "say -v Alex -o \\" & quoted form of outputFile & "\\ \\"" & {repr(text)} & "\\""
'''
    
    start = time.time()
    
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        timeout=60
    )
    
    elapsed = time.time() - start
    
    if output_file.exists():
        audio_size = output_file.stat().st_size
    else:
        audio_size = 0
    
    return {
        "elapsed_ms": int(elapsed * 1000),
        "audio_size_bytes": audio_size,
        "success": output_file.exists(),
        "method": "AppleScript baseline"
    }


def benchmark_say_baseline(text):
    """Standard say command"""
    output_file = Path("/tmp/say_baseline.aiff")
    
    start = time.time()
    
    result = subprocess.run(
        ["say", "-v", "Alex", "-o", str(output_file), text],
        capture_output=True,
        timeout=60
    )
    
    elapsed = time.time() - start
    
    if output_file.exists():
        audio_size = output_file.stat().st_size
    else:
        audio_size = 0
    
    return {
        "elapsed_ms": int(elapsed * 1000),
        "audio_size_bytes": audio_size,
        "success": output_file.exists(),
        "method": "say command"
    }


import subprocess


def main():
    """Run benchmarks"""
    
    test_cases = [
        ("1 word", "Hello"),
        ("8 chars", "Hello world"),
        ("20 chars", "The quick brown fox jumps"),
        ("50 chars", "Welcome to our app. We are excited to have you here."),
    ]
    
    print("="*70)
    print("TTS BENCHMARK v6 - FIXED PYOBJC")
    print("="*70)
    
    results = {}
    
    for name, text in test_cases:
        print(f"\nBenchmarking: {name} ({len(text)} chars)")
        
        # Standard say
        results["say"] = benchmark_say_baseline(text)
        print(f"  say: {results['say']['elapsed_ms']}ms")
        
        # AppleScript
        results["applescript"] = benchmark_applescript_baseline(text)
        print(f"  AppleScript: {results['applescript']['elapsed_ms']}ms")
        
        # PyObjC
        results["pyobjc"] = benchmark_pyobjc_direct(text)
        print(f"  PyObjC: {results['pyobjc']['elapsed_ms']}ms")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    averages = {}
    for method in ["say", "applescript", "pyobjc"]:
        times = [results[method]["elapsed_ms"] for name, text in test_cases]
        averages[method] = sum(times) / len(times)
    
    print("\n--- Averages ---")
    for method, avg in averages.items():
        marker = "⚡" if avg == min(averages.values()) else ""
        print(f"  {method}: {avg:.1f}ms {marker}")
    
    best_method = min(averages, key=averages.get)
    print(f"\n✅ Best Method: {best_method} ({averages[best_method]:.1f}ms avg)")
    
    print(f"\n--- Target Check (250ms) ---")
    best_avg = averages[best_method]
    print(f"  Best Average: {best_avg:.1f}ms")
    print(f"  Target (250ms): {'✅ REACHED' if best_avg <= 250 else f'❌ {best_avg - 250:.0f}ms over target'}")


if __name__ == "__main__":
    main()
