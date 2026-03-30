import SwiftUI

struct ContentView: View {
    @Environment(\.synthesizer) var synthesizer
    
    @State private var text = ""
    @State private var isProcessing = false
    @State private var lastLatency: Double = 0
    @State private var selectedModel = "yourtts"
    
    let speakers = ["neutral", "male", "female"]
    @State private var selectedSpeakerIndex = 0
    
    var body: some View {
        VStack(spacing: 20) {
            HStack {
                Text("SwiftTTS")
                    .font(.largeTitle)
                    .bold()
                Spacer()
            }
            .padding(.top, 20)
            
            Picker("Model", selection: $selectedModel) {
                Text("YourTTS (Fast)").tag("yourtts")
                Text("Voxtral (Quality)").tag("voxtral")
            }
            .pickerStyle(SegmentedPickerStyle())
            .padding(.horizontal)
            
            TextEditor(text: $text)
                .frame(minHeight: 200)
                .padding()
                .border(Color.gray.opacity(0.3), width: 1)
                .padding(.horizontal)
            
            HStack {
                Text("Speaker:")
                    .font(.subheadline)
                Picker("", selection: $selectedSpeakerIndex) {
                    ForEach(0 ..< speakers.count) { i in
                        Text(speakers[i]).tag(i)
                    }
                }
                .pickerStyle(MenuPickerStyle())
            }
            .padding(.horizontal)
            
            Button(action: synthesize) {
                if isProcessing {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle())
                } else {
                    Label("Speak", systemImage: "speaker.wave.2")
                        .padding(.horizontal, 40)
                        .padding(.vertical, 12)
                }
            }
            .buttonStyle(BorderedProminentButtonStyle())
            .disabled(isProcessing || text.isEmpty)
            
            if lastLatency > 0 {
                Text(String(format: "Latency: %.2f ms", lastLatency))
                    .font(.caption)
                    .foregroundColor(.green)
            }
            
            Spacer()
        }
        .padding()
    }
    
    private func synthesize() {
        guard !text.isEmpty else { return }
        
        let speaker = speakers[selectedSpeakerIndex]
        isProcessing = true
        
        Task {
            let start = Date()
            
            do {
                if selectedModel == "yourtts" {
                    _ = try await synthesizer.synthesizeYourTTS(text: text, speaker: speaker)
                } else {
                    _ = try await synthesizer.synthesizeVoxtral(text: text, speaker: speaker)
                }
                
                let end = Date()
                lastLatency = end.timeIntervalSince(start) * 1000
                
            } catch {
                print("Error: \(error)")
            }
            
            isProcessing = false
        }
    }
}

// Custom environment key for passing synthesizer
extension EnvironmentValues {
    @Entry var synthesizer: TTSSynthesizer = TTSSynthesizer()
}
