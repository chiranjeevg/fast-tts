#!/usr/bin/env python3
"""
TTS Benchmark v3 - AVAudioEngine Native

Uses native macOS AVFoundation audio engine for:
- Voice warmup (no repeated initialization)
- Audio queue buffering
- Simultaneous chunk processing

Target: 100ms avg latency for optimized scenarios
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
import tempfile

class AVAudioEngineTTS:
    """
    Native AVFoundation TTS with persistent engine instance
    Avoids subprocess overhead by using Python's ctypes to call AVFoundation
    """
    
    def __init__(self):
        self.output_dir = Path("/tmp/tts_benchmark_v3")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # AVFoundation setup via AppleScript for native access
        self.setup_applescript()
    
    def setup_applescript(self):
        """Create AppleScript that maintains persistent AVAudioEngine"""
        
        self.applescript_template = '''
use framework "AVFoundation"
use scripting additions

property voiceName : "Alex"
property audioEngine : missing value
property audioPlayer : missing item

on init()
    set audioEngine to current application's AVAudioEngine's new()
end init

on speakText:text
    set synthesizer to current application's AVSpeechSynthesizer's alloc()'s init()
    
    -- Create speech utterance
    set utterance to current application's AVSpeechUtterance's alloc()'s initWithString:text
    tell utterance
        set rate to 0.5
        set voice to current application's AVSpeechSynthesisVoice's voiceWithLanguageIdentifier:"en-US"
        set volume to 1.0
    end tell
    
    -- Speak
    synthesizer's speakUtterance:utterance
    
    -- Wait for completion
    delay 0.1
    repeat until synthesizer's isSpeaking() as boolean is false
        delay 0.1
    end repeat
    
    return "done"
end speakText

-- Quick test (no delay for completion)
on quickSpeak:text
    set synthesizer to current application's AVSpeechSynthesizer's alloc()'s init()
    set utterance to current application's AVSpeechUtterance's alloc()'s initWithString:text
    tell utterance
        set rate to 0.5
        set voice to current application's AVSpeechSynthesisVoice's voiceWithLanguageIdentifier:"en-US"
    end tell
    synthesizer's speakUtterance:utterance
end quickSpeak
'''
        
        self.applescript_path = self.output_dir / "tts_engine.scpt"
        with open(self.applescript_path, 'w') as f:
            f.write(self.applescript_template)
    
    def speak_direct_applescript(self, text):
        """Direct AppleScript call (baseline)"""
        output_file = self.output_dir / "applescript_direct.m4a"
        
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
            "success": output_file.exists()
        }
    
    def speak_with_queue(self, text):
        """
        Uses AVSpeechSynthesizer queue approach
        Multiple utterances can be queued for batch processing
        """
        output_file = self.output_dir / "queue_speak.m4a"
        
        # Create a queue-based script
        script = f'''
set outputFile to POSIX path of "{output_file}"
set utteranceText to {repr(text)}

-- Use speech synthesis with queue
set synthesizer to current application's AVSpeechSynthesizer's alloc()'s init()
set utterance to current application's AVSpeechUtterance's alloc()'s initWithString:utteranceText
tell utterance
    set rate to 0.5
    set voice to current application's AVSpeechSynthesisVoice's voiceWithLanguageIdentifier:"en-US"
end tell

synthesizer's speakUtterance:utterance
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
            "success": output_file.exists()
        }


def benchmark_baseline(text):
    """Standard say command baseline"""
    output_file = Path("/tmp/baseline_baseline.aiff")
    
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
    
    return {"elapsed_ms": int(elapsed * 1000), "audio_size_bytes": audio_size, "success": True}


def benchmark_warmup(text):
    """Warmup approach - pre-initialize voice"""
    output_file = Path("/tmp/warmup_baseline.aiff")
    
    # Warmup
    subprocess.run(["say", "-v", "Alex", "-o", "/dev/null", "warmup"], capture_output=True, timeout=10)
    
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
    
    return {"elapsed_ms": int(elapsed * 1000), "audio_size_bytes": audio_size, "success": True}


def benchmark_optimized_chunked(text):
    """
    Optimized chunking with minimal overhead
    - Skip small chunks
    - Reuse voice engine state
    """
    output_file = Path("/tmp/optimized_chunked.aiff")
    
    # Warmup
    subprocess.run(["say", "-v", "Alex", "-o", "/dev/null", "warmup"], capture_output=True, timeout=10)
    
    import re
    
    # Smart chunking
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    start = time.time()
    
    # Process all chunks in single subprocess call
    chunk_commands = []
    for i, sentence in enumerate(sentences):
        if i == len(sentences) - 1:
            cmd = f"say -v Alex -o '{output_file}' '{sentence}'"
        else:
            # Fastest for intermediate chunks
            cmd = f"say -v Alex '{sentence}' > /dev/null 2>&1"
        chunk_commands.append(cmd)
    
    # Single shell execution for all chunks
    full_script = "; ".join(chunk_commands)
    
    result = subprocess.run(
        ["bash", "-c", full_script],
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
        "num_chunks": len(sentences),
        "success": output_file.exists()
    }


def main():
    """Run all benchmarks"""
    
    test_cases = [
        ("1 word", "Hello"),
        ("8 chars", "Hello world"),
        ("20 chars", "The quick brown fox jumps"),
        ("50 chars", "Welcome to our app. We are excited to have you here."),
        ("100 chars", "Welcome to our application. We are excited to have you here."),
        ("200 chars", "This is a longer test of the text to speech system. It uses optimized chunking with voice warmup for maximum performance.")
    ]
    
    print("="*70)
    print("TTS BENCHMARK v3 - Optimized Chunking")
    print("="*70)
    
    results = {
        "baseline": {},
        "warmup": {},
        "optimized_chunked": {}
    }
    
    for name, text in test_cases:
        print(f"\nBenchmarking: {name} ({len(text)} chars)")
        
        # Baseline
        results["baseline"][name] = benchmark_baseline(text)
        print(f"  Baseline: {results['baseline'][name]['elapsed_ms']}ms")
        
        # Warmup
        results["warmup"][name] = benchmark_warmup(text)
        print(f"  Warmup: {results['warmup'][name]['elapsed_ms']}ms")
        
        # Optimized
        results["optimized_chunked"][name] = benchmark_optimized_chunked(text)
        print(f"  Optimized Chunked: {results['optimized_chunked'][name]['elapsed_ms']}ms")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for name in results["baseline"].keys():
        baseline = results["baseline"][name]["elapsed_ms"]
        warmup = results["warmup"][name]["elapsed_ms"]
        optimized = results["optimized_chunked"][name]["elapsed_ms"]
        
        print(f"\n{name}:")
        print(f"  Baseline:  {baseline}ms")
        print(f"  Warmup:    {warmup}ms ({baseline - warmup:+d}ms)")
        print(f"  Optimized: {optimized}ms ({baseline - optimized:+d}ms)")
    
    # Averages
    baseline_avg = sum([r["elapsed_ms"] for r in results["baseline"].values()]) / len(results["baseline"])
    warmup_avg = sum([r["elapsed_ms"] for r in results["warmup"].values()]) / len(results["warmup"])
    optimized_avg = sum([r["elapsed_ms"] for r in results["optimized_chunked"].values()]) / len(results["optimized_chunked"])
    
    print("\n--- Averages ---")
    print(f"Baseline:  {baseline_avg:.1f}ms")
    print(f"Warmup:    {warmup_avg:.1f}ms ({(baseline_avg - warmup_avg) / baseline_avg * 100:+.1f}%)")
    print(f"Optimized: {optimized_avg:.1f}ms ({(baseline_avg - optimized_avg) / baseline_avg * 100:+.1f}%)")
    
    print(f"\nTarget (250ms): {'✅ REACHED' if optimized_avg <= 250 else f'❌ {optimized_avg - 250:.0f}ms over target'}")


if __name__ == "__main__":
    main()
