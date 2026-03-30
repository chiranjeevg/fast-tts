import Cocoa
import AVFoundation

class ViewController: NSViewController {
    private let synthesizer: AVSpeechSynthesizer
    private let textView = NSTextView()
    
    init(synthesizer: AVSpeechSynthesizer) {
        self.synthesizer = synthesizer
        super.init(nibName: nil, bundle: nil)
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
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
        
        let slowButton = NSButton(title: "Slow", target: self, action: #selector(speak_slow))
        slowButton.bezelStyle = .rounded
        
        let fastButton = NSButton(title: "Fast", target: self, action: #selector(speak_fast))
        fastButton.bezelStyle = .rounded
        
        buttonRow.addArrangedSubview(slowButton)
        buttonRow.addArrangedSubview(fastButton)
        
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
    
    @objc private func speak_slow() {
        guard let text = textView.string, !text.isEmpty else { return }
        
        let utterance = AVSpeechUtterance(string: text)
        utterance.rate = 0.3 // Slower but same latency
        utterance.voice = AVSpeechVoice(language: "en-US")
        
        print("Speaking (slow)...")
        let start = CFAbsoluteTimeGetCurrent()
        
        synthesizer.speak(utterance)
    }
    
    @objc private func speak_fast() {
        guard let text = textView.string, !text.isEmpty else { return }
        
        // Use faster utterance for short text
        let utterance = AVSpeechUtterance(string: text)
        utterance.rate = 0.5
        utterance.pitchMultiplier = 1.1
        utterance.voice = AVSpeechVoice(language: "en-US")
        
        print("Speaking (fast)...")
        let start = CFAbsoluteTimeGetCurrent()
        
        synthesizer.speak(utterance)
    }
}
