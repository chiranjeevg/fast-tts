import UIKit

class ViewController: UIViewController {
    private let textView = UITextView()
    private let synthesizer = TTSSynthesizer()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        view.backgroundColor = .white
        title = "SwiftTTS"
        
        setupUI()
    }
    
    private func setupUI() {
        textView.frame = view.bounds
        textView.textColor = .black
        textView.font = UIFont.systemFont(ofSize: 16)
        textView.backgroundColor = .white
        
        let speakButton = UIButton(type: .system)
        speakButton.setTitle("Speak", for: .normal)
        speakButton.addTarget(self, action: #selector(speak), for: .touchUpInside)
        
        let pickerView = UIPickerView()
        pickerView.dataSource = self
        pickerView.delegate = self
        
        let containerView = UIView()
        containerView.translatesAutoresizingMaskIntoConstraints = false
        
        textView.addSubview(speakButton)
        containerView.addSubview(pickerView)
        
        view.addSubview(textView)
        view.addSubview(containerView)
        
        NSLayoutConstraint.activate([
            textView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            textView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            textView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            
            containerView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            containerView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            containerView.topAnchor.constraint(equalTo: textView.bottomAnchor, constant: 16),
            containerView.heightAnchor.constraint(equalToConstant: 200)
        ])
        
        speakButton.translatesAutoresizingMaskIntoConstraints = false
        pickerView.translatesAutoresizingMaskIntoConstraints = false
        
        NSLayoutConstraint.activate([
            speakButton.leadingAnchor.constraint(equalTo: containerView.leadingAnchor, constant: 16),
            speakButton.trailingAnchor.constraint(equalTo: containerView.trailingAnchor, constant: -16),
            speakButton.topAnchor.constraint(equalTo: containerView.topAnchor, constant: 16),
            
            pickerView.leadingAnchor.constraint(equalTo: containerView.leadingAnchor),
            pickerView.trailingAnchor.constraint(equalTo: containerView.trailingAnchor),
            pickerView.topAnchor.constraint(equalTo: speakButton.bottomAnchor, constant: 16)
        ])
    }
    
    @objc private func speak() {
        guard let text = textView.text, !text.isEmpty else { return }
        
        synthesizer.speak(text) { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success:
                    print("✅ Audio played successfully")
                case .failure(let error):
                    print("❌ Error: \(error)")
                    self?.showAlert(message: "Playback failed: \(error.localizedDescription)")
                }
            }
        }
    }
    
    private func showAlert(message: String) {
        let alert = UIAlertController(title: "Error", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        present(alert, animated: true)
    }
}

extension ViewController: UIPickerViewDataSource, UIPickerViewDelegate {
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return synthesizer.speakers.count
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return synthesizer.speakers[row]
    }
}
