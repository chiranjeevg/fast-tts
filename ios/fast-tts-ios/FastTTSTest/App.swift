//
//  FastTTS iOS App
//  Fast-TTS: High-Performance Text-to-Speech for WhatsApp & Mobile
//
//  Created by Hermes Agent Team on 2026-03-29
//  Copyright (c) 2026 Hermes AI. All rights reserved.
//

import SwiftUI

@main
struct FastTTSTestApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
