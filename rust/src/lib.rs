pub mod yourtts;
pub mod voxtral;

use std::fs;
use std::path::Path;

/// Initialize the TTS engine
pub fn init() -> Result<(), String> {
    println!("TTS Engine initialized");
    Ok(())
}

/// Convert text to speech using YourTTS
pub fn synthesize_yourtts(text: &str, speaker_id: Option<&str>) -> Result<Vec<u8>, String> {
    yourtts::synthesis(text, speaker_id)
}

/// Convert text to speech using Voxtral
pub fn synthesize_voxtral(text: &str, speaker_id: Option<&str>) -> Result<Vec<u8>, String> {
    voxtral::synthesis(text, speaker_id)
}

/// Benchmark inference latency
pub fn benchmark(model: &str) -> Result<serde_json::Value, String> {
    let start = std::time::Instant::now();
    
    match model {
        "yourtts" => synthesize_yourtts("Hello world", None).map(|_| ())?,
        "voxtral" => synthesize_voxtral("Hello world", None).map(|_| ())?,
        _ => return Err(format!("Unknown model: {}", model)),
    }
    
    let elapsed = start.elapsed();
    Ok(serde_json::json!({
        "model": model,
        "latency_ms": elapsed.as_millis()
    }))
}
