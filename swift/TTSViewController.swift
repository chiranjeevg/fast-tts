import UIKit

/// Main view controller for TTS app
class TTSViewController: UIViewController {
    private let textView = UITextView()
    private let modelPicker = UIPickerView()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        title = "SwiftTTS"
        view.backgroundColor = .systemBackground
        
        setupUI()
    }
    
    private func setupUI() {
        // Text input
        textView.frame = CGRect(x: 20, y: 100, width: view.bounds.width - 40, height: 200)
        textView.font = UIFont.systemFont(ofSize: 16)
        textView.textColor = .secondaryLabel
        textView.backgroundColor = .systemGray6
        textView.layer.cornerRadius = 8
        textView.layer.borderWidth = 1
        textView.layer.borderColor = UIColor.systemGray4.cgColor
        textView.text = "Type something here..."
        
        view.addSubview(textView)
        
        // Model picker
        modelPicker.frame = CGRect(x: 20, y: 310, width: view.bounds.width - 40, height: 60)
        modelPicker.backgroundColor = .systemGray6
        view.addSubview(modelPicker)
        
        // Speak button
        let speakButton = UIButton(type: .system)
        speakButton.frame = CGRect(x: 20, y: 380, width: view.bounds.width - 40, height: 50)
        speakButton.setTitle("Speak", for: .normal)
        speakButton.titleLabel?.font = UIFont.boldSystemFont(ofSize: 20)
        speakButton.backgroundColor = .systemBlue
        speakButton.setTitleColor(.white, for: .normal)
        speakButton.layer.cornerRadius = 10
        speakButton.addTarget(self, action: #selector(speakTapped), for: .touchUpInside)
        
        view.addSubview(speakButton)
    }
    
    @objc private func speakTapped() {
        guard let text = textView.text, !text.isEmpty else {
            print("❌ No text to speak")
            return
        }
        
        print("🗣️ Speaking: \(text)")
        
        // TODO: Call Rust FFI
        // tts_engine_speak(text)
    }
}

extension TTSViewController: UIPickerViewDataSource, UIPickerViewDelegate {
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return 2 // YourTTS and Voxtral
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return row == 0 ? "YourTTS (fast)" : "Voxtral (high-quality)"
    }
}
