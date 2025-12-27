import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class DeepM3UCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("IPTV Deep Checker (Real Stream Validation with FFprobe)")
        self.root.geometry("750x550")
        
        # --- SETTINGS ---
        self.timeout = 7   # Max seconds to wait for a stream
        self.workers = 10  # FFprobe is heavy, do not increase too much (10–15 max)
        
        # FFprobe path (must be in the same folder or available in system PATH)
        self.ffprobe_path = "ffprobe.exe"

        # --- UI ---
        frame_top = tk.Frame(root, pady=10)
        frame_top.pack(fill="x")
        
        self.btn_select = tk.Button(
            frame_top,
            text="Select Folder & Start Deep Scan",
            command=self.start_thread,
            bg="#D32F2F",
            fg="white",
            font=("Arial", 11, "bold")
        )
        self.btn_select.pack(pady=5)
        
        info_lbl = tk.Label(
            frame_top,
            text=(
                "WARNING: This mode analyzes the actual stream using video codec inspection.\n"
                "It is slower but much more reliable.\n"
                "Make sure 'ffprobe.exe' is located next to this script."
            ),
            fg="#555"
        )
        info_lbl.pack()

        self.progress = ttk.Progressbar(root, orient="horizontal", length=650, mode="determinate")
        self.progress.pack(pady=10)
        
        self.lbl_stats = tk.Label(
            root,
            text="Total: 0 | Alive Streams: 0 | Dead/Broken: 0",
            font=("Arial", 10, "bold")
        )
        self.lbl_stats.pack(pady=5)

        self.log_area = scrolledtext.ScrolledText(root, width=85, height=20, font=("Consolas", 8))
        self.log_area.pack(pady=10, padx=10)

        self.is_running = False
        self.alive_count = 0
        self.dead_count = 0

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def check_stream_validity(self, url):
        """
        Uses FFprobe to check if the stream contains a real video stream.
        """
        if not url.startswith("http"):
            return False

        command = [
            self.ffprobe_path,
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=codec_type",
            "-of", "default=noprint_wrappers=1:nokey=1",
            "-timeout", str(self.timeout * 1000000),
            "-i", url
        ]

        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout
            )

            return "video" in result.stdout

        except subprocess.TimeoutExpired:
            return False
        except FileNotFoundError:
            self.log("ERROR: ffprobe.exe not found! Make sure it is next to the script.")
            return False
        except Exception:
            return False

    def start_thread(self):
        if self.is_running:
            return
        
        if not os.path.exists(self.ffprobe_path):
            self.log("⚠️ WARNING: ffprobe.exe not found next to the script. If not installed globally, it will fail.")

        folder_selected = filedialog.askdirectory()
        if not folder_selected:
            return

        self.is_running = True
        self.btn_select.config(state="disabled")
        self.log_area.delete('1.0', tk.END)
        self.log(f"Selected Folder: {folder_selected}")
        
        threading.Thread(
            target=self.process_folder,
            args=(folder_selected,),
            daemon=True
        ).start()

    def process_folder(self, folder_path):
        m3u_files = [f for f in os.listdir(folder_path) if f.endswith('.m3u') or f.endswith('.m3u8')]
        
        if not m3u_files:
            self.log("❌ No .m3u or .m3u8 files found in the folder.")
            self.reset_ui()
            return

        self.log(f"📂 {len(m3u_files)} playlist(s) will be analyzed. Deep scan may take some time...\n")

        for filename in m3u_files:
            filepath = os.path.join(folder_path, filename)
            self.process_single_file(filepath)

        self.log("\n🎉 DEEP CLEANING COMPLETED!")
        messagebox.showinfo("Completed", "All playlists were tested and cleaned using FFprobe.")
        self.reset_ui()

    def process_single_file(self, filepath):
        self.log(f"--- File: {os.path.basename(filepath)} ---")
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        playlist_items = []
        header_line = None
        first_line = lines[0] if lines and lines[0].startswith("#EXTM3U") else "#EXTM3U\n"

        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF"):
                header_line = line
            elif line.startswith("http") and header_line:
                playlist_items.append((header_line, line))
                header_line = None

        file_total = len(playlist_items)
        if file_total == 0:
            return

        self.progress["maximum"] = file_total
        self.progress["value"] = 0
        
        valid_items = []

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            future_to_item = {
                executor.submit(self.check_stream_validity, item[1]): item
                for item in playlist_items
            }

            completed_count = 0
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                is_working = future.result()
                
                completed_count += 1
                self.progress["value"] = completed_count
                
                if is_working:
                    valid_items.append(item)
                    self.alive_count += 1
                else:
                    self.dead_count += 1
                
                if completed_count % 2 == 0:
                    self.lbl_stats.config(
                        text=f"Processed: {completed_count}/{file_total} | Alive: {self.alive_count} | Dead: {self.dead_count}"
                    )
                    self.root.update_idletasks()

        if valid_items:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(first_line)
                for head, url in valid_items:
                    f.write(f"{head}\n{url}\n")
            self.log(f"   ✅ {os.path.basename(filepath)} updated. ({len(valid_items)} working streams)\n")
        else:
            self.log(f"   ❌ {os.path.basename(filepath)} emptied (no working streams found).\n")

    def reset_ui(self):
        self.is_running = False
        self.btn_select.config(state="normal")
        self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = DeepM3UCleaner(root)
    root.mainloop()
