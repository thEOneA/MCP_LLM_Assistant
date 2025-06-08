# Buddie 🌱

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/MemX-Workspace/Bud-App/pulls)

**BUDDIE** is a mobile application designed to be your centralized life hub, seamlessly recording all personal information (work, life, entertainment, etc.) while delivering enhanced AI interactions. For optimal experience, pair it with our companion smart earphones.

## ✨ Key Features
- Context-aware dialogue
- Hands-free interaction
- Meeting support
  - Meeting Summaries
  - Instant hints
  - Works with your current meeting styles
- Personalized assistance
  - Always-Ready Assistant
  - Daily Recap
  - Offers tailored suggestions
- Cross-platform support (iOS/Android)

## 🚀 Quick Start

### Prerequisites
- Flutter
- Android Studio / Xcode

### Installation
```bash
# Clone repository
git clone https://github.com/MemX-Workspace/Bud-App.git

# Install dependencies
cd Bud-App
flutter pub get

# Release an Android apk
flutter build apk --release

# Launch on Android or an Android emulator
flutter run
```

## 📱 User Guide

1. The app will guide you through 30-second voiceprint registration when first launched.
2. For enhanced voice features with Buddie headphones:
  - Open Settings in app
  - Select "Connect"
  - Ensure earphones are already paired in the system
  - Confirm connection in app

## 🛠️ Tech Stack

- **Frontend Framework**: Flutter
- **State Management**: Provider
- **Database**: ObjectBox

## 🌐 MCP Servers

This repository includes example MCP servers that expose additional tools over
WebSockets.

- **Weather MCP** (`lib/mcp/mcp_server.py`) provides weather forecasts (port
  8080).
- **Jokes MCP** (`lib/mcp/jokes_mcp_server.py`) returns a random programming
  joke via the `get-joke` tool (port 8081).
- **Calendar MCP** (`lib/mcp/calendar_mcp_server.py`) schedules meetings (port
  8082).
- **Travel MCP** (`lib/mcp/travel_mcp_server.py`) plans travel itineraries
  (port 8083).
- **Local Info MCP** (`lib/mcp/local_info_mcp_server.py`) suggests nearby
  points of interest (port 8084).
- **Geolocation MCP** (`lib/mcp/geolocation_mcp_server.py`) resolves IP
  addresses to a location (port 8085).

Run a server with:

```bash
pip install aiohttp websockets
python lib/mcp/<server_file>.py
```


## 🤝 Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository 
2. Create your feature branch (git checkout -b feature-AmazingFeature)
3. Commit changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature-AmazingFeature)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

## 📧 Contact

Issue Tracker: https://github.com/MemX-Workspace/Bud-App/issues
