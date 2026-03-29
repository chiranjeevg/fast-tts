//! TTS Engine - C bindings for Swift/Firebase
//!
//! Generated from Rust using bindgen

#ifndef TTSModule_h
#define TTSModule_h

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/// Model types
typedef enum {
    MODEL_YOURTTS = 0,
    MODEL_VOXTRAL = 1,
} ModelType;

/// Inference result
typedef struct {
    float* samples;
    size_t sample_count;
    uint32_t sample_rate;
    double latency_ms;
} InferenceResult;

/// Initialize TTS engine
void tts_init(void);

/// Generate speech from text (must free result after use)
InferenceResult tts_speak(const char* text, ModelType model);

/// Free inference result
void tts_free_result(InferenceResult* result);

/// Get available speakers for a model
const char** tts_get_speakers(ModelType model, size_t* count);

/// Free speakers list
void tts_free_speakers(const char** speakers, size_t count);

#ifdef __cplusplus
}
#endif
