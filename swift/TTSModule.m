//! C bindings for Rust TTS engine

#include "TTSModule.h"
#include <stdlib.h>
#include <string.h>

// Link against Rust library
extern void rust_tts_init(void);
extern void* rust_tts_speak(const char* text, int model_type);
extern void rust_tts_free_result(void* result_ptr);
extern const char** rust_tts_get_speakers(int model_type, size_t* count);
extern void rust_tts_free_speakers(const char** speakers, size_t count);

void tts_init(void) {
    rust_tts_init();
}

InferenceResult tts_speak(const char* text, ModelType model) {
    void* result_ptr = rust_tts_speak(text, (int)model);
    
    if (!result_ptr) {
        return (InferenceResult){0};
    }
    
    InferenceResult* rust_result = (InferenceResult*)result_ptr;
    InferenceResult swift_result = *rust_result;
    
    // Deep copy samples to Swift-managed memory
    if (swift_result.sample_count > 0) {
        swift_result.samples = (float*)malloc(swift_result.sample_count * sizeof(float));
        memcpy(swift_result.samples, rust_result->samples, swift_result.sample_count * sizeof(float));
    }
    
    return swift_result;
}

void tts_free_result(InferenceResult* result) {
    if (result->samples) {
        free(result->samples);
        result->samples = NULL;
    }
}

const char** tts_get_speakers(ModelType model, size_t* count) {
    return rust_tts_get_speakers((int)model, count);
}

void tts_free_speakers(const char** speakers, size_t count) {
    rust_tts_free_speakers(speakers, count);
}
