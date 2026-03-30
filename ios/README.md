# 📱 Fast-TTS iOS App

> Real-time WhatsApp message synthesis with native macOS audio backend

## Overview

The Fast-TTS iOS app demonstrates:

- ⚡ Instant voice responses (12ms cached synthesis)
- 🔄 Background caching for known messages
- 📱 Native iOS audio playback
- 🔗 WhatsApp Webhook integration

## Architecture

```
┌─────────────────────────────────────────────┐
│           iOS App (SwiftUI)                  │
│  ┌──────────────────┬────────────────────┐  │
│  │   Main View      │   Settings         │  │
│  └────────┬─────────┴──────────┬──────────┘  │
│           │                     │             │
│           ▼                     ▼             │
│  ┌──────────────────┐   ┌─────────────────┐ │
│  │ TTS Client       │   │ Audio Engine    │ │
│  └────────┬─────────┘   └────────┬────────┘ │
│           │                       │            │
│           ▼                       ▼            │
│  ┌──────────────────┐   ┌─────────────────┐ │
│  │ Cache Manager    │   │ HTTP Client     │ │
│  └──────────────────┘   └────────┬────────┘ │
│                                  │            │
│                                  ▼            │
│                         ┌─────────────────┐  │
│                         │  Backend API    │  │
│                         └─────────────────┘  │
└──────────────────────────────────────────────┘
```

## Features

### Core Functionality

- **Real-time TTS**: Instant audio playback for WhatsApp messages
- **Smart Caching**: SHA-256 content hashing with local cache
- **Background Processing**: Offload synthesis to background queue
- **Auto-retry**: Handle network failures gracefully

### Technical Details

| Component | Implementation |
|-----------|----------------|
| **Language** | Swift 5.7+ with SwiftUI |
| **Backend Integration** | URLSession for HTTP requests |
| **Audio Playback** | AVFoundation (AVPlayer) |
| **Caching** | UserDefaults + FileManager |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/fast-tts.git
cd fast-tts/ios

# Open in Xcode
open FastTTSTest.xcodeproj

# Build and run on simulator or device
```

## Project Structure

```
ios/
├── FastTTSTest/                  # Main app target
│   ├── AppDelegate.swift         # App lifecycle management
│   ├── SceneDelegate.swift       # Scene configuration
│   └── Resources/                # Assets and resources
├── FastTTSTests/                 # Unit tests
└── FastTTSUITests/               # UI tests
```

## API Integration

### Request Structure

```json
{
  "message": "Hello world!",
  "voice_id": "alex",
  "cache_key": "sha256_hash"
}
```

### Response Structure

```json
{
  "audio_url": "file:///tmp/audio.aiff",
  "cached": true,
  "latency_ms": 12
}
```

## Performance Characteristics

| Metric | Value |
|--------|-------|
| **Cold Start** | <50ms |
| **Cached Response** | ~12ms |
| **Cache Hit Rate** | 95%+ (real-world) |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

MIT - See `LICENSE` file for details.
