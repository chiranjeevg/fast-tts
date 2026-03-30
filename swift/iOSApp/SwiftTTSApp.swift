import SwiftUI

@main
struct SwiftTTSApp: App {
    @StateObject private var synthesizer = TTSSynthesizer()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.synthesizer, synthesizer)
        }
    }
}

// Custom environment key for passing synthesizer
extension EnvironmentValues {
    @Entry var synthesizer: TTSSynthesizer = TTSSynthesizer()
}
