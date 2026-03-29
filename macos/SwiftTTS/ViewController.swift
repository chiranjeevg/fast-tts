import Cocoa

class ViewController: NSViewController {
    private let textView = NSTextView()
    private let synthesizer = TTSSynthesizer()
    
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
        
        let pickerView = NSComboBox()
        pickerView.delegate = synthesizer
        pickerView.indexOfItem(withObjectValue: "neutral")
        
        let containerView = NSView()
        containerView.translatesAutoresizingMaskIntoConstraints = false
        
        view.addSubview(scrollView)
        view.addSubview(containerView)
        containerView.addSubview(pickerView)
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
            
            pickerView.leadingAnchor.constraint(equalTo: containerView.leadingAnchor),
            pickerView.trailingAnchor.constraint(equalTo: containerView.trailingAnchor),
            pickerView.topAnchor.constraint(equalTo: speakButton.bottomAnchor, constant: 16)
        ])
    }
    
    @objc private func speak() {
        guard let text = textView.string, !text.isEmpty else { return }
        
        synthesizer.speak(text) { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success:
                    print("✅ Audio played successfully")
                case .failure(let error):
                    self?.showAlert(message: "Playback failed: \(error.localizedDescription)")
                }
            }
        }
    }
    
    private func showAlert(message: String) {
        let alert = NSAlert()
        alert.messageText = "Error"
        alert.informativeText = message
        alert.addButton(withTitle: "OK")
        alert.alertStyle = .critical
        alert.beginSheetModal(for: view.window!)
    }
}
