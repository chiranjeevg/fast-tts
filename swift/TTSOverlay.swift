import SwiftUI

/// Overlay for displaying inference latency and model status
struct TTSOverlay: View {
    @State private var isProcessing = false
    @State private var latencyMs: Double = 0.0
    @State private var modelType: String = "YourTTS"
    @State private var errorMessage: String?
    
    @Environment(\.presentationMode) var presentationMode
    
    var body: some View {
        VStack(spacing: 20) {
            HStack {
                Text("TTS Engine")
                    .font(.headline)
                    .padding()
                
                Button(action: { presentationMode.wrappedValue.dismiss() }) {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundColor(.gray)
                }
            }
            
            Divider()
            
            if let error = errorMessage {
                Text(error)
                    .foregroundColor(.red)
                    .padding()
            } else if isProcessing {
                ProgressView("Generating speech...")
                    .padding()
            } else {
                Text("Ready")
                    .foregroundColor(.green)
                    .padding()
            }
            
            HStack {
                Picker("Model", selection: $modelType) {
                    Text("YourTTS (fast)").tag("YourTTS")
                    Text("Voxtral (high-quality)").tag("Voxtral")
                }
                .pickerStyle(SegmentedPickerStyle())
                .padding()
                
                Button("Speak") {
                    speak()
                }
                .buttonStyle(.borderedProminent)
                .padding()
            }
            
            if latencyMs > 0 {
                HStack {
                    Spacer()
                    Text(String(format: "Latency: %.1fms", latencyMs))
                        .font(.caption)
                        .foregroundColor(.blue)
                    Spacer()
                }
            }
        }
        .padding()
    }
    
    private func speak() {
        isProcessing = true
        errorMessage = nil
        
        // TODO: Call Rust FFI function
        // let result = tts_speak("Hello world", modelType)
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
            isProcessing = false
        }
    }
}

struct TTSOverlay_Previews: PreviewProvider {
    static var previews: some View {
        TTSOverlay()
    }
}
