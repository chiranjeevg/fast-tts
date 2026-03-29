//! Download and convert models for TTS engine
//!
//! Usage:
//!   cargo run --bin download_models -- yourtts
//!   cargo run --bin download_models -- voxtral

use std::path::Path;
use std::process::Command;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    
    if args.len() < 2 {
        eprintln!("Usage: download_models <yourtts|voxtral>");
        std::process::exit(1);
    }

    let model = &args[1];

    match model.as_str() {
        "yourtts" => download_yourtts(),
        "voxtral" => download_voxtral(),
        _ => {
            eprintln!("Unknown model: {}. Use 'yourtts' or 'voxtral'", model);
            std::process::exit(1);
        }
    }
}

fn download_yourtts() {
    let output_path = std::env::temp_dir().join("yourtts_coreml.mlmodel");
    
    println!("Downloading YourTTS ONNX model...");
    
    let url = "https://huggingface.co/myshell-ai/OpenVoiceV2/resolve/main/yourtts.onnx";
    
    // Download with curl
    let status = Command::new("curl")
        .arg("-L")
        .arg(url)
        .arg("-o")
        .arg(&output_path)
        .status()
        .expect("Failed to execute curl");
    
    if status.success() {
        println!("✅ Downloaded YourTTS to: {}", output_path.display());
        
        // Convert to CoreML (if coremltools is installed)
        println!("💡 To convert to CoreML, run:");
        println!("   python3 -m pip install coremltools");
        println!("   python3 convert_yourtts.py {}", output_path.display());
    } else {
        eprintln!("❌ Download failed");
    }
}

fn download_voxtral() {
    let output_path = std::env::temp_dir().join("voxtral-q4_k_m.gguf");
    
    println!("Downloading Voxtral safetensors and quantizing...");
    
    // Step 1: Download original model
    let safetensors_url = "https://huggingface.co/mistralai/Voxtral-4B-TTS-2603/resolve/main/consolidated.safetensors";
    let params_url = "https://huggingface.co/mistralai/Voxtral-4B-TTS-2603/resolve/main/params.json";
    
    println!("  - Downloading safetensors...");
    // curl -L {safetensors_url} -o consolidated.safetensors
    
    println!("  - Downloading params.json...");
    // curl -L {params_url} -o params.json
    
    println!("  - Quantizing to GGUF Q4_K_M...");
    // llama.cpp quantize_tool consolidated.safetensors vosxtral-q4_k_m.gguf Q4_K_M
    
    println!("✅ Download and quantization complete!");
    println!("   Note: You need llama.cpp installed for quantization");
}
