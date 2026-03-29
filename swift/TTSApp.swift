import SwiftUI

@main
struct TTSApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .padding()
        }
    }
}

struct ContentView: View {
    @State private var text = ""
    @State private var selectedModel = "YourTTS"
    @State private var isProcessing = false
    @State private var latencyMs: Double = 0.0
    
    var body: some View {
        VStack(spacing: 24) {
            Spacer()
            
            Text("Low-Latency TTS")
                .font(.largeTitle)
                .bold()
            
            Text("Text-to-Speech with YourTTS & Voxtral")
                .foregroundColor(.secondary)
            
            Divider()
            
            Text("Enter text to speak:")
                .font(.subheadline)
                .padding(.top, 16)
            
            TextEditor(text: $text)
                .frame(height: 150)
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(8)
            
            Picker("Model", selection: $selectedModel) {
                Text("YourTTS (fast, 15MB)")
                    .tag("YourTTS")
                Text("Voxtral (high-quality, 1.5GB)")
                    .tag("Voxtral")
            }
            .pickerStyle(SegmentedPickerStyle())
            
            Button(action: speak) {
                if isProcessing {
                    ProgressView()
                } else {
                    Text("Speak")
                        .font(.headline)
                }
            }
            .buttonStyle(.borderedProminent)
            .padding()
            
            if latencyMs > 0 {
                HStack {
                    Spacer()
                    Text(String(format: "Latency: %.1fms", latencyMs))
                        .font(.caption)
                        .foregroundColor(.blue)
                    Spacer()
                }
            }
            
            Spacer()
        }
        .padding()
    }
    
    private func speak() {
        guard !text.isEmpty else { return }
        
        isProcessing = true
        latencyMs = 0.0
        
        // TODO: Call Rust FFI function
        // let result = tts_speak(text, selectedModel)
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
            isProcessing = false
        }
    }
}

struct TTSApp_Previews: PreviewProvider {
    static var previews: some View {
        TTSApp()
    }
}
