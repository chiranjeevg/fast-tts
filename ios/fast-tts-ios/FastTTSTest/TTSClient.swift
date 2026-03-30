//
//  TTSClient.swift
//  FastTTSTest
//
//  Created by Hermes Agent Team on 2026-03-29.
//

import Foundation
import Combine

struct TTSRequest: Encodable {
    let message: String
    let voice_id: String = "alex"
    let cache_key: String?
}

struct TTSResponse: Decodable {
    let audio_url: String?
    let cached: Bool
    let latency_ms: Int
    let num_chunks: Int?
}

enum TTSResult {
    case success(TTSResponse)
    case failure(Error)
}

class TTSClient: ObservableObject {
    private let baseURL = "http://localhost:8000"
    
    func synthesize(text: String, completion: @escaping (TTSResult) -> Void) {
        var request = URLRequest(url: URL(string: "\(baseURL)/synthesize")!)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let cacheKey = text.sha256()
        let body = TTSRequest(message: text, cache_key: cacheKey)
        
        do {
            request.httpBody = try JSONEncoder().encode(body)
        } catch {
            completion(.failure(error))
            return
        }
        
        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            guard let self = self else { return }
            
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let data = data else {
                completion(.failure(NSError(domain: "No data", code: -1)))
                return
            }
            
            do {
                let response = try JSONDecoder().decode(TTSResponse.self, from: data)
                completion(.success(response))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
    
    func getAudio(for text: String, completion: @escaping (String?) -> Void) {
        synthesize(text: text) { result in
            switch result {
            case .success(let response):
                completion(response.audio_url)
            case .failure:
                completion(nil)
            }
        }
    }
}

extension String {
    func sha256() -> String {
        let data = Data(self.utf8)
        let hash = data.sha256()
        return hash.map { String(format: "%02x", $0) }.joined()
    }
}

extension Data {
    func sha256() -> [UInt8] {
        var hash = [UInt8](repeating: 0, count: Int(CC_SHA256_DIGEST_LENGTH))
        withUnsafeBytes { buffer in
            CC_SHA256(buffer.baseAddress, CC_LONG(count), &hash)
        }
        return hash
    }
}
