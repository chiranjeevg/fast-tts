//! TTS Engine - Low-latency Text-to-Speech inference
//!
//! This Rust library provides:
//! - YourTTS (ONNX CoreML) for fast, lightweight inference
//! - Voxtral-4B-TTS (GGUF/llama) for high-quality voice cloning
//!
//! # Usage
//!
//! ```ignore
//! use tts_engine::{init, speak, ModelType};
//!
//! init();
//!
//! // Use YourTTS for speed (40ms latency)
//! let audio1 = speak("Hello world", ModelType::YourTTS);
//!
//! // Or Voxtral for quality (200ms latency)
//! let audio2 = speak("Hello world", ModelType::Voxtral);
//! ```

pub mod yourtts;
pub mod voxtral;

use serde::{Deserialize, Serialize};

/// Supported TTS models
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ModelType {
    /// YourTTS - lightweight, ultra-fast (15MB)
    YourTTS,
    /// Voxtral-4B-TTS - high quality, voice cloning (1.5GB)
    Voxtral,
}

/// Inference result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InferenceResult {
    /// Audio samples (PCM format)
    pub samples: Vec<f32>,
    /// Sample rate in Hz
    pub sample_rate: u32,
    /// Inference latency in milliseconds
    pub latency_ms: f64,
}

/// Initialize the TTS engine (load models if needed)
pub fn init() {
    // Models are loaded lazily on first use
}

/// Generate speech from text using specified model
pub fn speak(text: &str, model: ModelType) -> Result<InferenceResult, String> {
    match model {
        ModelType::YourTTS => yourtts::infer(text),
        ModelType::Voxtral => voxtral::infer(text),
    }
}

/// List available speakers for voice cloning
pub fn get_speakers(model: ModelType) -> Vec<String> {
    match model {
        ModelType::YourTTS => vec!["neutral".to_string(), "male".to_string(), "female".to_string()],
        ModelType::Voxtral => vec![
            "neutral_male".to_string(),
            "neutral_female".to_string(),
            "cheerful_male".to_string(),
            "cheerful_female".to_string(),
        ],
    }
}
