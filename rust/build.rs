//! Build script for TTS engine
//!
//! Compiles CoreML models to native binaries for iOS/macOS

fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=models/");

    // TODO: Compile CoreML models
    // Use `coremlc` compiler to convert .mlmodel → .mlmodelc (compiled)
    // This is faster on Apple devices
}
