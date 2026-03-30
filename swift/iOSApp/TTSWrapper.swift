import Foundation

class TTSSynthesizer {
    static let shared = TTSSynthesizer()
    
    enum Error: LocalizedError {
        case synthesisFailed(String)
        
        var errorDescription: String? {
            switch self {
            case .synthesisFailed(let msg): return msg
            }
        }
    }
    
    init() {
        print("Initializing TTS engine...")
    }
    
    func synthesizeYourTTS(text: String, speaker: String? = nil) async throws -> Data {
        print("Synthesizing with YourTTS...")
        
        // TODO: Call Rust library via FFI
        throw Error.synthesisFailed("Rust backend not yet linked")
    }
    
    func synthesizeVoxtral(text: String, speaker: String? = nil) async throws -> Data {
        print("Synthesizing with Voxtral...")
        
        // TODO: Call Rust library via FFI
        throw Error.synthesisFailed("Rust backend not yet linked")
    }
}
