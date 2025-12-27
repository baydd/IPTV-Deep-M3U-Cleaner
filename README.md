# IPTV Deep M3U Cleaner

A desktop tool that **deeply validates IPTV streams** inside `.m3u` / `.m3u8` playlists using **FFprobe**.

Unlike simple HTTP checks, this tool verifies whether a stream actually contains a **real video stream**.

---

## 🚀 Features

- Deep IPTV stream validation using FFprobe
- Detects real video codecs (not fake or dead links)
- Multi-threaded scanning for faster processing
- Automatically cleans broken streams from playlists
- Simple GUI built with Tkinter
- Works locally (no external APIs)

---

## 🧠 How It Works

1. Reads `.m3u` / `.m3u8` playlist files
2. Extracts stream URLs
3. Uses **FFprobe** to analyze each stream
4. Keeps only streams that contain a valid video track
5. Overwrites the playlist with working streams only

This makes the results **much more reliable** than normal ping or HTTP status checks.

---

## 🖥 Requirements

- **Python 3.9+**
- **FFmpeg (ffprobe required)**

### FFprobe Setup

- Download FFmpeg from: https://ffmpeg.org/download.html
- Place `ffprobe.exe` in the same folder as the script  
  **OR**
- Make sure FFprobe is available in your system PATH

---

## ▶️ How to Use

1. Clone the repository:
   ```bash
  git clone https://github.com/baydd/IPTV-Deep-M3U-Cleaner.git
