# AgniNode Documentation & Field Demonstration Portal

Official documentation, video demonstrations, and NCRB fire casualty analysis reports for **AgniNode: Autonomous Fire Detection & Suppression System**.

## 🚀 Live Portal & Scanner Link

**Public URL:** [https://avishkarranjane.github.io/agninode-docs/](https://avishkarranjane.github.io/agninode-docs/)

Scan any of the provided QR codes in `assets/qr/` (`AgniNode_QR_Public.png`, `AgniNode_QR_Clean.png`, or `AgniNode_Scan_Card.png`) with any smartphone camera (iPhone Camera, Android, Google Lens, or WhatsApp scanner) to open the portal and access:

1. **AgniNode Working Demonstration** (`assets/videos/agninode-working.mp4` - 01:00 min) — End-to-end hardware workflow showing automated sensor detection, buzzer relay, and autonomous suppression sequence.
2. **Aerosol Module Working Test** (`assets/videos/aerosol-module-working.mp4` - 00:11 sec) — Rapid condensed aerosol discharge envelope test demonstrating microsecond flame reaction disruption.
3. **NCRB Deaths due to Accidental Fire in India (2021-2025)** (`assets/docs/ncrb-accidental-fire-deaths.pdf`) — National mortality breakdown and structural fire risk factors.
4. **NCRB Deaths due to Electrical Short Circuit Fires in India (2021-2025)** (`assets/docs/ncrb-electrical-short-circuit-fires.pdf`) — Empirical analysis of electrical short circuits as the primary source of urban fire fatalities.
5. **Reducing Electrical Fire Deaths in India: Components and Evidence** (`assets/docs/reducing-electrical-fire-deaths.pdf`) — Component-level engineering evidence proving how sub-second localized suppression eliminates flashover risk.

---

## 📁 Clean Project Architecture

```text
AgniNode Document/
├── assets/
│   ├── videos/             # Field test videos & poster thumbnails
│   │   ├── agninode-working.mp4
│   │   ├── aerosol-module-working.mp4
│   │   ├── poster-agninode.jpg
│   │   └── poster-aerosol.jpg
│   ├── docs/               # Official NCRB & technical research PDFs
│   │   ├── ncrb-accidental-fire-deaths.pdf
│   │   ├── ncrb-electrical-short-circuit-fires.pdf
│   │   └── reducing-electrical-fire-deaths.pdf
│   └── qr/                 # High-resolution scannable QR codes & placards
│       ├── AgniNode_QR_Public.png
│       ├── AgniNode_QR_Clean.png
│       ├── AgniNode_QR_Public.svg
│       ├── AgniNode_Scan_Card.png
│       ├── AgniNode_Scan_Card_Light.png
│       ├── AgniNode_QR_Local_WiFi.png
│       └── AgniNode_Scan_Card_Local_WiFi.png
├── index.html              # Main web portal
├── print-qr.html           # A4 printable placard & stickers
├── generate_qr_codes.py    # Python script for generating QR codes
├── server.py               # Local offline Wi-Fi streaming server
├── start_local_server.bat  # 1-click local server startup
├── README.md               # Project documentation
├── .gitignore              # Ignores __pycache__ and temp files
└── .nojekyll               # GitHub Pages static asset bypass
```

---

## ⚡ Video Playback & Mobile Compatibility

- Both MP4 files have been re-indexed with **FastStart (`moov` atom at file beginning)** for instantaneous streaming without buffering delays.
- Videos are formatted in universal **H.264 video + AAC audio** with `playsinline` support for native mobile playback on iOS Safari, Android Chrome, and Samsung Internet.
- PDF documents include 1-tap direct reader links, native mobile viewing, and local download options.
