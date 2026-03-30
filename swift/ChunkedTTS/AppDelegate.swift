import Cocoa

@main
class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    
    func applicationDidFinishLaunching(_ aNotification: Notification) {
        window = NSWindow(
            contentRect: NSMakeRect(0, 0, 500, 400),
            styleMask: [.titled, .closable],
            backing: .buffered,
            defer: false
        )
        
        window.title = "Chunked Streaming TTS"
        window.center()
        
        let controller = ViewController()
        window.contentViewController = controller
        window.makeKeyAndOrderFront(nil)
    }
}
