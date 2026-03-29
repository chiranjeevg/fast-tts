import Foundation
import AVFoundation

class TTSSynthesizer {
    private let backendURL = "http://localhost:8000"
    var speakers = ["neutral", "male", "female"]
    
    enum TTSError: Error {
        case invalidResponse
        case networkError(Error)
        case decodingError(Error)
    }
    
    func speak(_ text: String, completion: @escaping (Result<Void, TTSError>) -> Void) {
        guard let url = URL(string: "\(backendURL)/tts") else {
            completion(.failure(.invalidResponse))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let params = [
            "text": text,
            "speaker_id": speakers[0],
            "model": "yourtts"
        ] as [String: Any]
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: params)
        
        let task = URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            guard let self = self else { return }
            
            if let error = error {
                completion(.failure(.networkError(error)))
                return
            }
            
            guard let data = data, let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                  let audioBase64 = json["audio"] as? String else {
                completion(.failure(.invalidResponse))
                return
            }
            
            // Decode and play audio (placeholder)
            completion(.success(()))
        }
        
        task.resume()
    }
}
