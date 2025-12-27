IPTV Deep M3U Cleaner

IPTV Deep M3U Cleaner is a desktop application that deeply validates IPTV streams inside .m3u / .m3u8 playlists using FFprobe.

Unlike basic HTTP or ping-based checkers, this tool verifies whether a stream actually contains a real video stream, making the results far more reliable.

<img width="753" height="580" alt="image" src="https://github.com/user-attachments/assets/d29ff2e3-fe74-49eb-8f75-ddc898af7a98" />

<img width="745" height="581" alt="image" src="https://github.com/user-attachments/assets/8e358a50-f278-42e6-848c-4f3e5238415e" />

✨ Features

Deep IPTV stream validation with FFprobe

Detects real video codecs, not just reachable URLs

Removes dead, fake, or broken streams

Multi-threaded scanning for better performance

Simple and clean Tkinter GUI

Works fully offline / locally

Automatically updates playlists in-place

🧠 How It Works

Reads .m3u / .m3u8 playlist files

Extracts stream URLs

Uses FFprobe to inspect stream codecs

Keeps only streams that contain a valid video track

Overwrites the playlist with working streams only

This approach is slower than simple checks, but much more accurate.

🖥 Requirements

Python 3.9+

FFmpeg (ffprobe required)

⚙️ FFprobe Setup
Option 1 (Recommended – Windows)

Download FFmpeg from
https://ffmpeg.org/download.html

Extract it

Copy ffprobe.exe next to the Python script

Option 2 (System-wide)

Install FFmpeg and make sure ffprobe is available in your system PATH

▶️ How to Use

Clone the repository:

git clone https://github.com/baydd/IPTV-Deep-M3U-Cleaner.git


Run the application:

python deep.py


Click "Select Folder & Start Deep Scan"

Choose a folder containing .m3u or .m3u8 files

Wait for the scan to finish

✔ Your playlists will be cleaned automatically
✔ Only working streams will remain

⏱ Performance Notes

Deep scan is intentionally slower than simple link checkers

Large playlists may take several minutes

Increasing thread count too much may overload FFprobe and reduce stability

⚠️ Disclaimer

This project is intended for playlist maintenance and testing purposes only.
Users are responsible for ensuring their playlists comply with applicable laws.

📜 License

MIT License
Free to use, modify, and distribute.

🤝 Contributing

Pull requests and improvements are welcome.
Feel free to fork the project and enhance it.

⭐ Support

If this project helped you, please consider giving it a star ⭐ on GitHub.
