//
//  ContentView.swift
//  FastTTSTest
//
//  Created by Hermes Agent Team on 2026-03-29.
//

import SwiftUI

struct ContentView: View {
    @State private var inputText = "Hello, Fast-TTS!"
    @State private var isPlaying = false
    @State private var audioURL: String?
    
    let ttsClient = TTSClient()
    
    var body: some View {
        VStack(spacing: 24) {
            Text("Fast-TTS")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Text("High-Performance Text-to-Speech")
                .font(.headline)
                .foregroundColor(.secondary)
            
            VStack(alignment: .leading, spacing: 16) {
                Text("Enter message to synthesize:")
                    .font(.subheadline)
                    .fontWeight(.semibold)
                
                TextEditor(text: $inputText)
                    .frame(minHeight: 120)
                    .padding()
                    .border(Color.gray.opacity(0.3), width: 1)
                    .cornerRadius(8)
                
                Button(action: synthesize) {
                    HStack {
                        Spacer()
                        if isPlaying {
                            Spinner()
                        } else {
                            Image(systemName: "speaker.wave.2")
                        }
                        Spacer()
                        Text("Synthesize")
                            .font(.headline)
                    }
                    .padding()
                }
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(8)
                
                if let audioURL = audioURL {
                    AudioPlayerView(audioURL: audioURL, isPlaying: $isPlaying)
                        .padding()
                }
            }
            .padding()
            
            Spacer()
        }
        .padding()
    }
    
    private func synthesize() {
        guard !inputText.isEmpty else { return }
        
        isPlaying = true
        
        ttsClient.synthesize(text: inputText) { [weak self] result in
            guard let self = self else { return }
            
            DispatchQueue.main.async {
                self.isPlaying = false
                
                switch result {
                case .success(let response):
                    if let audioURL = response.audio_url {
                        self.audioURL = audioURL
                    }
                case .failure(let error):
                    print("Error: \(error)")
                }
            }
        }
    }
}

struct AudioPlayerView: View {
    let audioURL: String
    @State private var player: AVAudioPlayer?
    @Binding var isPlaying: Bool
    
    var body: some View {
        HStack(spacing: 16) {
            Button(action: togglePlay) {
                Image(systemName: isPlaying ? "pause.circle" : "play.circle")
                    .font(.largeTitle)
            }
            
            Text("Audio")
                .font(.subheadline)
                .foregroundColor(.secondary)
            
            Spacer()
        }
        .onAppear {
            setupPlayer()
        }
    }
    
    private func setupPlayer() {
        guard let url = URL(string: audioURL) else { return }
        
        do {
            player = try AVAudioPlayer(contentsOf: url)
            player?.delegate = self
        } catch {
            print("Error setting up player: \(error)")
        }
    }
    
    private func togglePlay() {
        guard let player = player else { return }
        
        if isPlaying {
            player.pause()
        } else {
            player.play()
        }
        
        self.isPlaying.toggle()
    }
}

extension AudioPlayerView: AVAudioPlayerDelegate {
    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        isPlaying = false
    }
}
