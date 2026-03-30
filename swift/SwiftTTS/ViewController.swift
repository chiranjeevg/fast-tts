import Cocoa
import AVFoundation

class ViewController: NSViewController {
    private let synthesizer = AVSpeechSynthesizer()
    private let textView = NSTextView()
    
    override func loadView() {
        view = NSView()
        view.translatesAutoresizingMaskIntoConstraints = false
        view.backgroundColor = .white
        
        setupUI()
    }
    
    private func setupUI() {
        let scrollView = NSScrollView()
        scrollView.translatesAutoresizingMaskIntoConstraints = false
        scrollView.hasVerticalScroller = true
        
        textView.frame = NSMakeRect(0, 0, 560, 200)
        textView.isHorizontallyScrollable = false
        textView.textContainer?.widthTracksTextView = true
        
        scrollView.documentView = textView
        
        let speakButton = NSButton(title: "Speak", target: self, action: #selector(speak))
        speakButton.bezelStyle = .rounded
        speakButton.translatesAutoresizingMaskIntoConstraints = false
        
        let voicesPicker = NSComboBox()
        voicesPicker.addItem(withObjectValue: "Alex")
        voicesPicker.addItem(withObjectValue: "Samantha")
        voicesPicker.addItem(withObjectValue: "Victoria")
        voicesPicker.selectItem(at: 0)
        voicesPicker.translatesAutoresizingMaskIntoConstraints = false
        
        let containerView = NSView()
        containerView.translatesAutoresizingMaskIntoConstraints = false
        
        view.addSubview(scrollView)
        view.addSubview(containerView)
        containerView.addSubview(voicesPicker)
        containerView.addSubview(speakButton)
        
        NSLayoutConstraint.activate([
            scrollView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            scrollView.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),
            scrollView.topAnchor.constraint(equalTo: view.topAnchor, constant: 40),
            
            containerView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            containerView.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),
            containerView.topAnchor.constraint(equalTo: scrollView.bottomAnchor, constant: 20),
            
            speakButton.leadingAnchor.constraint(equalTo: containerView.leadingAnchor, constant: 16),
            speakButton.trailingAnchor.constraint(equalTo: containerView.trailingAnchor, constant: -16),
            speakButton.topAnchor.constraint(equalTo: containerView.topAnchor, constant: 16),
            
            voicesPicker.leadingAnchor.constraint(equalTo: containerView.leadingAnchor),
            voicesPicker.trailingAnchor.constraint(equalTo: containerView.trailingAnchor),
            voicesPicker.topAnchor.constraint(equalTo: speakButton.bottomAnchor, constant: 16)
        ])
    }
    
    @objc private func speak() {
        guard let text = textView.string, !text.isEmpty else { return }
        
        let utterance = AVSpeechUtterance(string: text)
        if let voiceName = voicesPicker?.itemObjectValue as? String {
            utterance.voice = AVSpeechVoice(language: "en-US")
            utterance.rate = 0.5
        }
        
        synthesizer.speak(utterance)
    }
    
    private var voicesPicker: NSComboBox?
}
