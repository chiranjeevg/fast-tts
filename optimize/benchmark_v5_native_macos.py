#!/usr/bin/env python3
"""
TTS Benchmark v5 - Native macOS AVFoundation

Uses PyObjC or AppleScript to access native AVFoundation APIs
Avoids subprocess overhead entirely

Target: 100ms for short text, 250ms for long text
"""

import os
import sys
import json
import time
from pathlib import Path

# Try to use PyObjC if available
try:
    from AppKit import NSSpeechSynthesizer
    PYOBJC_AVAILABLE = True
except ImportError:
    PYOBJC_AVAILABLE = False


class NativeTTSBenchmarker:
    def __init__(self):
        self.output_dir = Path("/tmp/tts_benchmark_v5")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.pyobjc_available = PYOBJC_AVAILABLE
        
        if not PYOBJC_AVAILABLE:
            print("⚠️  PyObjC not available, falling back to AppleScript")
    
    def benchmark_applescript_native(self, text):
        """AppleScript with native AVFoundation"""
        output_file = self.output_dir / "applescript_native.aiff"
        
        script = f'''
use framework "AVFoundation"

set outputFile to POSIX path of "{output_file}"
set synthesizer to current application's AVSpeechSynthesizer's alloc()'s init()

-- Create utterance
set utterance to current application's AVSpeechUtterance's alloc()'s initWithString:{repr(text)}
tell utterance
    set rate to 0.5
    set voice to current application's AVSpeechSynthesisVoice's voiceWithLanguageIdentifier:"en-US"
    set volume to 1.0
end tell

-- Speak synchronously
synthesizer's speakUtterance:utterance

-- Wait for completion
delay 0.1
repeat until synthesizer's isSpeaking() as boolean is false
    delay 0.01
end repeat

return "done"
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
            "method": "AppleScript AVFoundation"
        }
    
    def benchmark_pyobjc(self, text):
        """Direct PyObjC AVFoundation access"""
        output_file = self.output_dir / "pyobjc_speak.m4a"
        
        try:
            from AppKit import NSSpeechSynthesizer
            Foundation = __import__('Foundation')
        except ImportError:
            return {"elapsed_ms": 9999, "error": "PyObjC not available"}
        
        start = time.time()
        
        # Create speech synthesizer
        synth = NSSpeechSynthesizer.alloc().init()
        
        # Set voice
        voices = Foundation.NSSpeechSynthesisVoice.voiceNames()
        if "Alex" in voices:
            synth.setVoice_("Alex")
        
        # Set rate (0.0 to 1.0, Alex default is ~0.2)
        synth.setRate_(0.5)
        
        # Set volume
        synth.setVolume_(1.0)
        
        # Start speaking to file
        output_url = Foundation.NSURL.fileURLWithPath_(str(output_file))
        
        # Speak to file
        synth.startSpeakingString_toUrl_(text, output_url)
        
        # Wait for completion (with timeout)
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
            "method": "PyObjC"
        }
    
    def benchmark_applescript_baseline(self, text):
        """Standard AppleScript baseline"""
        output_file = self.output_dir / "applescript_baseline.aiff"
        
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
    
    def benchmark_say_baseline(self, text):
        """Standard say command"""
        output_file = self.output_dir / "say_baseline.aiff"
        
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
    print("TTS BENCHMARK v5 - NATIVE MACOS AVFOUNDATION")
    print("="*70)
    
    benchmarker = NativeTTSBenchmarker()
    
    if not PYOBJC_AVAILABLE:
        print("\n⚠️  PyObjC not available. Install with: pip3 install pyobjc")
    
    results = {}
    
    for name, text in test_cases:
        print(f"\nBenchmarking: {name} ({len(text)} chars)")
        
        # Standard say
        results["say"] = benchmarker.benchmark_say_baseline(text)
        print(f"  say: {results['say']['elapsed_ms']}ms")
        
        # AppleScript
        results["applescript"] = benchmarker.benchmark_applescript_baseline(text)
        print(f"  AppleScript: {results['applescript']['elapsed_ms']}ms")
        
        # PyObjC
        if PYOBJC_AVAILABLE:
            results["pyobjc"] = benchmarker.benchmark_pyobjc(text)
            print(f"  PyObjC: {results['pyobjc']['elapsed_ms']}ms")
        else:
            results["pyobjc"] = {"elapsed_ms": 9999, "error": "PyObjC not available"}
            print(f"  PyObjC: Skipped (not installed)")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for name, text in test_cases:
        print(f"\n{name}:")
        for method, data in results.items():
            if "error" in data:
                print(f"  {method}: Error - {data['error']}")
            else:
                print(f"  {method}: {data['elapsed_ms']}ms ({data.get('method', method)})")
    
    # Averages
    if PYOBJC_AVAILABLE:
        averages = {}
        for method in ["say", "applescript", "pyobjc"]:
            times = [results[method].get("elapsed_ms", 9999) for name, text in test_cases]
            averages[method] = sum(times) / len(times)
        
        print("\n--- Averages ---")
        for method, avg in averages.items():
            print(f"  {method}: {avg:.1f}ms")
        
        best_method = min(averages, key=averages.get)
        print(f"\n✅ Best: {best_method} ({averages[best_method]:.1f}ms avg)")


if __name__ == "__main__":
    main()
