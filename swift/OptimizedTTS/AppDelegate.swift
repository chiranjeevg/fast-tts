import Cocoa

class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    var synthesizer = AVSpeechSynthesizer()
    
    func applicationDidFinishLaunching(_ aNotification: Notification) {
        // Pre-warm the synthesizer to reduce first utterance latency
        warmupSynthesizer()
        
        // Create main window
        window = NSWindow(
            contentRect: NSMakeRect(0, 0, 600, 400),
            styleMask: [.titled, .closable, .resizable],
            backing: .buffered,
            defer: false
        )
        
        window.title = "Optimized TTS Benchmark"
        window.center()
        window.makeKeyAndOrderFront(nil)
        
        setupUI()
    }
    
    private func warmupSynthesizer() {
        print("Pre-warming synthesizer...")
        
        let utterance = AVSpeechUtterance(string: "warmup")
        utterance.rate = 0.5
        
        synthesizer.speak(utterance)
        
        // Wait a bit for warmup to complete
        Thread.sleep(forTimeInterval: 0.2)
        
        synthesizer.stopSpeaking(at: .immediate)
        
        print("Synthesizer pre-warmed")
    }
    
    private func setupUI() {
        guard let content = window.contentView else { return }
        
        let stackView = NSStackView()
        stackView.orientation = .vertical
        stackView.spacing = 20
        stackView.translatesAutoresizingMaskIntoConstraints = false
        
        // Input field
        let inputField = NSTextField()
        inputField.placeholderString = "Enter text to synthesize..."
        inputField.translatesAutoresizingMaskIntoConstraints = false
        
        // Button row
        let buttonRow = NSStackView()
        buttonRow.orientation = .horizontal
        buttonRow.spacing = 10
        buttonView.translatesAutoresizingMaskIntoConstraints = false
        
        // Test buttons for different text lengths
        let shortButton = NSButton(title: "Short (10 chars)", target: self, action: #selector(testShort))
        let mediumButton = NSButton(title: "Medium (50 chars)", target: self, action: #selector(testMedium))
        let longButton = NSButton(title: "Long (150 chars)", target: self, action: #selector(testLong))
        
        buttonRow.addArrangedSubview(shortButton)
        buttonRow.addArrangedSubview(mediumButton)
        buttonRow.addArrangedSubview(longButton)
        
        // Results display
        let resultTextView = NSTextView()
        resultTextView.string = "Benchmark results will appear here..."
        resultTextView.isEditable = false
        
        let scrollView = NSScrollView()
        scrollView.documentView = resultTextView
        scrollView.translatesAutoresizingMaskIntoConstraints = false
        scrollView.hasVerticalScroller = true
        scrollView.documentView?.frame.size.height = 150
        
        // Metrics display
        let metricsLabel = NSTextField(labelWithString: "Latency: --ms")
        metricsLabel.font = NSFont.monospacedSystemFont(ofSize: 14, weight: .bold)
        metricsLabel.backgroundColor = NSColor.systemGray6
        
        // Add to stack
        stackView.addArrangedSubview(inputField)
        stackView.addArrangedSubview(buttonRow)
        stackView.addArrangedSubview(scrollView)
        stackView.addArrangedSubview(metricsLabel)
        
        content.addSubview(stackView)
        
        NSLayoutConstraint.activate([
            stackView.leadingAnchor.constraint(equalTo: content.leadingAnchor, constant: 20),
            stackView.trailingAnchor.constraint(equalTo: content.trailingAnchor, constant: -20),
            stackView.topAnchor.constraint(equalTo: content.topAnchor, constant: 40),
            
            scrollView.heightAnchor.constraint(equalToConstant: 150)
        ])
    }
    
    @objc private func testShort() {
        let text = "Hello world, this is a short test."
        runBenchmark(text: text)
    }
    
    @objc private func testMedium() {
        let text = "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet and is commonly used for typing practice."
        runBenchmark(text: text)
    }
    
    @objc private func testLong() {
        let text = "Welcome to our application. We are excited to have you here today. Our platform provides powerful text-to-speech capabilities that can transform written content into natural sounding audio. The system supports multiple languages and voice options to suit your needs."
        runBenchmark(text: text)
    }
    
    private func runBenchmark(text: String) {
        print("\n=== BENCHMARK START ===")
        print("Text length: \(text.count) chars")
        
        // Apple AVFoundation (no chunking)
        let avfoundationTime = measureAVFoundation(text: text)
        
        // Chunked AVFoundation
        let chunkedTime = measureChunkedAVFoundation(text: text)
        
        // Print results
        print("\nRESULTS:")
        print("  Apple AVFoundation:     \(avfoundationTime)ms")
        print("  Chunked AVFoundation:   \(chunkedTime)ms")
        
        if avfoundationTime > 0 {
            let improvement = ((avfoundationTime - chunkedTime) / avfoundationTime * 100)
            print("  Improvement:            \(improvement)%")
        }
        
        // Print to UI
        let results = """
        Text: \(text.prefix(50))...
        
        AVFoundation Time:     \(avfoundationTime)ms
        Chunked Time:          \(chunkedTime)ms
        
        improvement:           \(improvement)% reduction
        """
        
        print("RESULTS:\n" + results)
    }
    
    private func measureAVFoundation(text: String) -> Int {
        let start = CFAbsoluteTimeGetCurrent()
        
        let utterance = AVSpeechUtterance(string: text)
        utterance.rate = 0.5
        utterance.pitchMultiplier = 1.0
        utterance.volume = 1.0
        
        synthesizer.speak(utterance)
        
        // Wait for completion
        while synthesizer.isSpeaking {
            RunLoop.current.run(until: Date(timeIntervalSinceNow: 0.1))
        }
        
        return Int((CFAbsoluteTimeGetCurrent() - start) * 1000)
    }
    
    private func measureChunkedAVFoundation(text: String) -> Int {
        let start = CFAbsoluteTimeGetCurrent()
        
        // Split into chunks
        let sentences = text.components(separatedBy: ". ")
        
        for (index, sentence) in sentences.enumerated() {
            let cleanSentence = sentence.trimmingCharacters(in: .whitespaces)
            guard !cleanSentence.isEmpty else { continue }
            
            let fullSentence = cleanSentence + "."
            let utterance = AVSpeechUtterance(string: fullSentence)
            utterance.rate = 0.5
            utterance.pitchMultiplier = 1.0
            
            if index < sentences.count - 1 {
                // Non-final chunks
                utterance.volume = 0.0  // Mute, but still process
            }
            
            synthesizer.speak(utterance)
        }
        
        // Wait for completion
        while synthesizer.isSpeaking {
            RunLoop.current.run(until: Date(timeIntervalSinceNow: 0.1))
        }
        
        return Int((CFAbsoluteTimeGetCurrent() - start) * 1000)
    }
    
    func applicationShouldTerminate(_ sender: NSApplication) -> Bool {
        synthesizer.stopSpeaking(at: .immediate)
        return true
    }
}
