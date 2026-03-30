import Cocoa

@main
class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    private let synthesizer = AVSpeechSynthesizer()
    
    func applicationDidFinishLaunching(_ aNotification: Notification) {
        // Pre-warm on app launch
        prewarm()
        
        window = NSWindow(
            contentRect: NSMakeRect(0, 0, 500, 350),
            styleMask: [.titled, .closable],
            backing: .buffered,
            defer: false
        )
        
        window.title = "Streaming TTS"
        window.center()
        
        let controller = ViewController(synthesizer: synthesizer)
        window.contentViewController = controller
        window.makeKeyAndOrderFront(nil)
    }
    
    private func prewarm() {
        // Pre-load the synthesis engine
        let utterance = AVSpeechUtterance(string: "prewarm")
        utterance.rate = 0.1
        utterance.voice = AVSpeechVoice(language: "en-US")
        
        synthesizer.speak(utterance)
        
        DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + 0.15) {
            self.synthesizer.stopSpeaking(at: .immediate)
            print("✓ Engine pre-warmed in ~150ms")
        }
    }
}
