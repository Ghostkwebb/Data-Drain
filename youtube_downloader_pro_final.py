import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import json
import re
import os
import sys
import requests
from PIL import Image, ImageTk
from io import BytesIO
import queue

def get_executable_path(name):
    """Gets the absolute path to a bundled executable."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, name)
    return name

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.COLOR = {
            'bg': '#1E1E1E', 'frame': '#2D2D2D', 'text': '#EAEAEA', 'entry_bg': '#252526',
            'accent': '#007FFF', 'accent_fg': '#FFFFFF', 'disabled_fg': '#8A8A8A', 'border': '#555555'
        }
        self.root = root
        self.root.title("DataDrain")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLOR['bg'])

        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('.', background=self.COLOR['bg'], foreground=self.COLOR['text'], fieldbackground=self.COLOR['entry_bg'], borderwidth=1, lightcolor=self.COLOR['border'], darkcolor=self.COLOR['border'])
        style.map('.', background=[('active', self.COLOR['frame'])])
        style.configure('TFrame', background=self.COLOR['bg'])
        style.configure('TLabel', font=('SF Pro Text', 13), background=self.COLOR['bg'], foreground=self.COLOR['text'])
        style.configure('Header.TLabel', font=('SF Pro Display', 20, 'bold'))
        style.configure('Title.TLabel', font=('SF Pro Display', 15, 'bold'), anchor='center')
        style.configure('Status.TLabel', font=('SF Pro Text', 12), anchor='center')
        style.configure('TEntry', font=('SF Pro Text', 13), foreground=self.COLOR['text'])
        style.configure('TCombobox', font=('SF Pro Text', 13), arrowsize=20)
        style.map('TCombobox', fieldbackground=[('readonly', self.COLOR['entry_bg'])], foreground=[('readonly', self.COLOR['text']), ('disabled', self.COLOR['disabled_fg'])])
        style.map('TEntry', foreground=[('readonly', self.COLOR['text'])])
        style.configure('TButton', font=('SF Pro Display', 13, 'bold'), padding=12, relief='flat', borderwidth=0)
        style.configure('Accent.TButton', background=self.COLOR['accent'], foreground=self.COLOR['accent_fg'])
        style.map('Accent.TButton', background=[('active', '#005f9e'), ('disabled', self.COLOR['frame'])], foreground=[('disabled', self.COLOR['disabled_fg'])])
        style.configure('Icon.TButton', font=('SF Pro Text', 14))
        style.configure('TProgressbar', thickness=6, troughcolor=self.COLOR['frame'], background=self.COLOR['accent'], borderwidth=0)

        main_frame = ttk.Frame(root, width=500)
        main_frame.pack(expand=True, padx=30, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)

        url_section = ttk.Frame(main_frame)
        url_section.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        ttk.Label(url_section, text="Video URL", style='Header.TLabel').pack(anchor='center', pady=(0, 10))
        url_frame = ttk.Frame(url_section)
        url_frame.pack(fill=tk.X)
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=('SF Pro Text', 14), justify='center')
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, ipadx=5)
        self.fetch_button = ttk.Button(url_frame, text="🔎", style='Icon.TButton', command=self.fetch_video_info, width=2)
        self.fetch_button.pack(side=tk.LEFT, padx=(10, 0))

        self.results_frame = ttk.Frame(main_frame)
        self.results_frame.grid(row=1, column=0, sticky='ew', pady=15)
        self.thumb_label = ttk.Label(self.results_frame, anchor='center')
        self.thumb_label.pack()
        self.title_label = ttk.Label(self.results_frame, text="", style='Title.TLabel', wraplength=480)
        self.title_label.pack(pady=(15, 5))

        self.options_frame = ttk.Frame(main_frame)
        self.options_frame.grid(row=2, column=0, sticky='ew')
        self.options_frame.columnconfigure(1, weight=1)
        for i, label_text in enumerate(["Quality:", "Format:", "Save To:"]):
            ttk.Label(self.options_frame, text=label_text).grid(row=i, column=0, sticky='w', pady=8, padx=(5,15))

        self.quality_var = tk.StringVar()
        self.quality_menu = ttk.Combobox(self.options_frame, textvariable=self.quality_var, state='disabled', justify='center')
        self.quality_menu.grid(row=0, column=1, columnspan=2, sticky='ew', ipady=4, pady=5)

        self.format_var = tk.StringVar()
        self.format_menu = ttk.Combobox(self.options_frame, textvariable=self.format_var, state='disabled', justify='center')
        self.format_menu.grid(row=1, column=1, columnspan=2, sticky='ew', ipady=4, pady=5)

        self.path_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        path_entry_frame = ttk.Frame(self.options_frame)
        path_entry_frame.grid(row=2, column=1, sticky='ew', pady=5)
        path_entry = ttk.Entry(path_entry_frame, textvariable=self.path_var, state='readonly')
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, ipadx=5)
        self.browse_button = ttk.Button(self.options_frame, text="📁", style='Icon.TButton', command=self.browse_path, width=2)
        self.browse_button.grid(row=2, column=2, padx=10)

        self.quality_menu.bind("<<ComboboxSelected>>", self.on_quality_selected)

        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, sticky='ew', pady=(25, 0))
        self.download_button_text = tk.StringVar(value="⬇️ Download")
        self.download_button = ttk.Button(action_frame, textvariable=self.download_button_text, style='Accent.TButton', command=self.download_video, state='disabled')
        self.download_button.pack(fill=tk.X, ipady=8)

        self.status_label = ttk.Label(action_frame, text="Enter a video URL to begin.", style='Status.TLabel')
        self.status_label.pack(fill=tk.X, pady=(12, 8))
        self.progress_bar = ttk.Progressbar(action_frame)
        self.progress_bar.pack(fill=tk.X, ipady=3)

        self.video_data, self.thumbnail_image, self.process = None, None, None
        self._reset_ui(initial_load=True)

    def fetch_video_info(self):
        if not self.url_var.get():
            return
        self._reset_ui(partial=True)
        self.set_ui_state('disabled')
        self.status_label.config(text="⏳ Fetching video information...")
        self.progress_bar.config(mode='indeterminate')
        self.progress_bar.start(10)
        threading.Thread(target=self._fetch_thread, args=(self.url_var.get(),), daemon=True).start()

    def _fetch_thread(self, url):
        try:
            yt_dlp_path = get_executable_path('yt-dlp')
            cmd = [yt_dlp_path, '--dump-json', '--no-warnings', url]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=20, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            self.video_data = json.loads(result.stdout)
            self.root.after(0, self._update_ui_with_video_data)
        except Exception as e:
            self.root.after(0, self._handle_error, "Fetch Error", f"Failed to fetch video.\n{e}")

    def _update_ui_with_video_data(self):
        self.progress_bar.stop()
        self.progress_bar.config(mode='determinate')
        self.results_frame.grid()
        self.options_frame.grid()
        self.title_label.config(text=self.video_data.get('title', 'N/A'))

        unique_qualities = sorted(list(set((f['height'], f.get('fps', 0)) for f in self.video_data['formats'] if f.get('vcodec') != 'none' and f.get('height'))), key=lambda x: (x[0], x[1]), reverse=True)
        display_qualities = [f"{h}p @ {fps}fps" for h, fps in unique_qualities if fps]
        display_qualities.insert(0, "Best Available")
        display_qualities.append("Audio Only")
        self.quality_menu['values'] = display_qualities
        self.quality_menu.current(0)
        self.on_quality_selected()

        if thumbnail_url := self.video_data.get('thumbnail'):
            threading.Thread(target=self._load_thumbnail, args=(thumbnail_url,), daemon=True).start()

        self.status_label.config(text="✅ Video loaded. Choose options and download.")
        self.set_ui_state('normal')

    def on_quality_selected(self, event=None):
        if self.quality_var.get() == "Audio Only":
            self.format_menu['values'] = ['mp3 (Standard)', 'wav (Lossless)', 'flac (Lossless)', 'm4a (Apple Standard)']
        else:
            self.format_menu['values'] = ['mp4 (For QuickTime)', 'mkv (Best Quality)', 'mov (For Editing)', 'avi (Legacy)']
        self.format_menu.current(0)
        self.format_menu.config(state='readonly')
        self.download_button.config(state='normal')

    def download_video(self):
        self.set_ui_state('disabled')
        self.progress_bar['value'] = 0
        self.is_processing = False
        threading.Thread(target=self._download_thread, daemon=True).start()

    def _enqueue_output(self, stream, q):
        for line in iter(stream.readline, ''):
            q.put(line)
        stream.close()

    def _process_queue(self):
        try:
            while True:
                line = self.queue.get_nowait()
                self._update_progress(line)
                if "error" in line.lower() and self.process.poll() is not None:
                    self.stderr_output += line + "\n"
        except queue.Empty:
            pass
        finally:
            if self.process and self.process.poll() is None:
                self.root.after(100, self._process_queue)
            else:
                self.finalize_download()

    def finalize_download(self):
        if self.process and self.process.returncode == 0:
            self._download_complete()
        else:
            self._handle_error("Download Error", self.stderr_output)

    def _download_thread(self):
        quality, container_choice, url = self.quality_var.get(), self.format_var.get(), self.url_var.get()
        container = container_choice.split(' ')[0]
        final_path = os.path.join(self.path_var.get(), f'%(title)s.{container}')
        yt_dlp_path = get_executable_path('yt-dlp')
        cmd = [
            yt_dlp_path, '--progress', '--no-warnings',
            '--ignore-config', '--no-mtime',
            '-o', final_path, url
        ]
        if hasattr(sys, '_MEIPASS'):
            cmd.extend(['--ffmpeg-location', get_executable_path('ffmpeg')])

        if quality == "Audio Only":
            cmd.extend(['-f', 'bestaudio', '-x', '--audio-format', container])
        else:
            if quality == "Best Available":
                format_selector = "bestvideo+bestaudio/best"
            else:
                match = re.search(r'(\d+)p @ (\d+\.?\d*)fps', quality)
                h, fps = match.groups()
                video_specs = f"[height<={h}][fps<={fps}]"
                format_selector = f"bestvideo{video_specs}"
            cmd.extend(['-f', format_selector])
            if container in ['mp4', 'mov', 'avi']:
                cmd.extend(['--recode-video', container])
            else:
                cmd.extend(['--merge-output-format', container])

        try:
            creationflags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True, creationflags=creationflags)
            self.queue = queue.Queue()
            self.stderr_output = ""
            threading.Thread(target=self._enqueue_output, args=(self.process.stdout, self.queue), daemon=True).start()
            self.root.after(100, self._process_queue)
        except Exception as e:
            self.root.after(0, self._handle_error, "Execution Error", str(e))

    def _update_progress(self, line):
        if not line:
            return

        processing_keywords = [
            "[merger]", "[extractaudio]", "[ffmpeg]",
            "merging formats", "re-encoding", "destination:"
        ]

        if any(keyword in line.lower() for keyword in processing_keywords):
            if not self.is_processing:
                self.is_processing = True
                self.progress_bar.config(mode='indeterminate')
                self.progress_bar.start(10)
                self.download_button_text.set("⚙️ Processing...")
                self.status_label.config(text="⚙️ Processing with FFmpeg... (This may take a moment)")

        elif "[download]" in line and not self.is_processing:
            self.progress_bar.config(mode='determinate')
            if match := re.search(r'([0-9.]+)%', line):
                percent = float(match.group(1))
                self.progress_bar['value'] = percent
                self.download_button_text.set(f"⬇️ Downloading... {percent:.1f}%")
                self.status_label.config(text=f"⬇️ {' '.join(line.split()[1:])}")

    def _download_complete(self):
        self.progress_bar.stop()
        self.progress_bar['value'] = 100
        self.status_label.config(text="✅ Download successful!")
        self.download_button_text.set("✅ Complete!")
        messagebox.showinfo("Success", f"Download complete!\nFile saved in: {self.path_var.get()}")
        self.root.after(2000, self._reset_ui)

    def _handle_error(self, title, message):
        self.progress_bar.stop()
        self.download_button_text.set("❌ Error")
        self.status_label.config(text=f"❌ {title}. See message for details.")
        detailed_message = message.strip() if message else "An unknown error occurred."
        if "ffmpeg" in detailed_message.lower() and "not found" in detailed_message.lower():
            messagebox.showerror(title, "FFmpeg not found. This is required.\nPlease install via Homebrew: `brew install ffmpeg`")
        else:
            messagebox.showerror(title, f"An error occurred:\n\n{detailed_message}")
        self.root.after(2000, self._reset_ui)

    def _reset_ui(self, clear_url=True, partial=False, initial_load=False):
        self.progress_bar.stop()
        self.progress_bar['value'] = 0
        if initial_load:
            self.results_frame.grid_remove()
            self.options_frame.grid_remove()
        if not partial:
            self.results_frame.grid_remove()
            self.options_frame.grid_remove()
            if clear_url:
                self.url_var.set("")
        self.download_button_text.set("⬇️ Download")
        self.status_label.config(text="Enter a new URL to begin.")
        self.set_ui_state('initial')

    def set_ui_state(self, state):
        status = 'normal' if state != 'disabled' else 'disabled'
        widgets_to_toggle = [self.fetch_button, self.browse_button, self.quality_menu, self.format_menu, self.download_button]
        for widget in widgets_to_toggle:
            widget.config(state=status)
        if state == 'initial':
            for widget in [self.quality_menu, self.format_menu, self.download_button]:
                widget.config(state='disabled')
        elif state == 'normal_after_download':
            self.download_button.config(state='normal')
        else:
            self.download_button.config(state='disabled')

    def _load_thumbnail(self, url):
        try:
            response = requests.get(url, timeout=10)
            img = Image.open(BytesIO(response.content))
            img.thumbnail((480, 270))
            self.thumbnail_image = ImageTk.PhotoImage(img)
            self.thumb_label.config(image=self.thumbnail_image)
        except Exception:
            self.thumb_label.config(text="🚫\nCould not load thumbnail")

    def browse_path(self):
        if self.browse_button['state'] != 'disabled':
            directory = filedialog.askdirectory(initialdir=self.path_var.get())
            if directory:
                self.path_var.set(directory)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()