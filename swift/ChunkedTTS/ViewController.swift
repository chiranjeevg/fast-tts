import Cocoa
import AVFoundation

class ViewController: NSViewController {
    private let synthesizer = AVSpeechSynthesizer()
    private let textView = NSTextView()
    private var latencyLabel: NSTextField!
    
    override func loadView() {
        view = NSView()
        view.translatesAutoresizingMaskIntoConstraints = false
        view.backgroundColor = .windowBackgroundColor
        
        setupUI()
    }
    
    private func setupUI() {
        let scrollView = NSScrollView()
        scrollView.translatesAutoresizingMaskIntoConstraints = false
        scrollView.hasVerticalScroller = true
        
        textView.frame = NSMakeRect(0, 0, 460, 150)
        textView.isHorizontallyScrollable = false
        textView.textContainer?.widthTracksTextView = true
        
        scrollView.documentView = textView
        
        let buttonRow = NSStackView()
        buttonRow.orientation = .horizontal
        buttonRow.spacing = 10
        buttonRow.translatesAutoresizingMaskIntoConstraints = false
        
        let fastButton = NSButton(title: "Fast", target: self, action: #selector(chunkedSpeak))
        fastButton.bezelStyle = .rounded
        fastButton.font = NSFont.systemFont(ofSize: 16, weight: .bold)
        
        latencyLabel = NSTextField(labelWithString: "Latency: --ms")
        latencyLabel.font = NSFont.monospacedSystemFont(ofSize: 12, weight: .regular)
        latencyLabel.backgroundColor = .systemGray6
        
        buttonRow.addArrangedSubview(fastButton)
        buttonRow.addArrangedSubview(latencyLabel)
        
        let container = NSView()
        container.translatesAutoresizingMaskIntoConstraints = false
        container.addSubview(scrollView)
        container.addSubview(buttonRow)
        
        view.addSubview(container)
        
        NSLayoutConstraint.activate([
            container.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            container.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),
            container.topAnchor.constraint(equalTo: view.topAnchor, constant: 40),
            
            scrollView.leadingAnchor.constraint(equalTo: container.leadingAnchor),
            scrollView.trailingAnchor.constraint(equalTo: container.trailingAnchor),
            scrollView.topAnchor.constraint(equalTo: container.topAnchor),
            scrollView.heightAnchor.constraint(equalToConstant: 150),
            
            buttonRow.leadingAnchor.constraint(equalTo: container.leadingAnchor),
            buttonRow.trailingAnchor.constraint(equalTo: container.trailingAnchor),
            buttonRow.topAnchor.constraint(equalTo: scrollView.bottomAnchor, constant: 20)
        ])
    }
    
    @objc private func chunkedSpeak() {
        guard let text = textView.string, !text.isEmpty else { return }
        
        // Split text into chunks (sentence-based)
        let sentences = splitIntoChunks(text: text)
        
        print("Speaking \(sentences.count) chunks...")
        let start = CFAbsoluteTimeGetCurrent()
        
        for (index, chunk) in sentences.enumerated() {
            let utterance = AVSpeechUtterance(string: chunk)
            utterance.rate = 0.5
            utterance.pitchMultiplier = 1.0
            utterance.volume = 1.0
            
            // Only wait for last chunk to complete
            if index < sentences.count - 1 {
                utterance.preUtterances = [] // Don't wait for other chunks
            }
            
            synthesizer.speak(utterance)
        }
    }
    
    private func splitIntoChunks(text: String) -> [String] {
        // Simple sentence splitting
        let sentences = text.components(separatedBy: ". ")
        
        // If no periods, try commas
        if sentences.count <= 1 {
            let chunks = text.components(separatedBy: ", ")
            return chunks.count > 1 ? chunks : [text]
        }
        
        // Re-join sentences with periods
        var result: [String] = []
        var currentChunk = ""
        
        for sentence in sentences {
            let cleanSentence = sentence.trimmingCharacters(in: .whitespaces)
            if cleanSentence.isEmpty { continue }
            
            let fullSentence = cleanSentence + "."
            
            if currentChunk.isEmpty {
                currentChunk = fullSentence
            } else {
                let combined = currentChunk + " " + fullSentence
                if combined.count < 80 { // Keep chunks under 80 chars
                    currentChunk = combined
                } else {
                    result.append(currentChunk)
                    currentChunk = fullSentence
                }
            }
        }
        
        if !currentChunk.isEmpty {
            result.append(currentChunk)
        }
        
        return result
    }
}
