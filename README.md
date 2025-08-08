# DataDrain 排水

![DataDrain Screenshot]([https://github.com/user-attachments/assets/5e54acd8-78c0-4d6f-9d67-d2cecc3a0a55)
![DataDrain Screenshot]([https://github.com/user-attachments/assets/2ce6ff46-e0de-42ec-87f4-b2395c428d63)

<img width="600" height="828" alt="Screenshot 2025-08-08 at 7 15 52 PM" src="https://github.com/user-attachments/assets/a7fd4ad4-678f-4ddf-8cda-edd4c2376519" />
<img width="600" height="828" alt="Screenshot 2025-08-08 at 7 16 15 PM" src="https://github.com/user-attachments/assets/d8b2895f-d34f-4458-a5a9-2a735571adec" />


A simple, modern, and powerful YouTube downloader for macOS and Windows, built with Python and `yt-dlp`. DataDrain offers a clean, dark-themed interface to download any video or audio from YouTube in your desired format and quality.

---

## ✨ Features

-   **Modern Dark UI**: A clean, professionally designed dark theme that's easy on the eyes.
-   **Fetch Video Details**: Instantly fetches and displays the video thumbnail and title when you paste a link.
-   **Advanced Quality Selection**: Choose from a complete list of available resolutions and frame rates (e.g., `4K @ 60fps`).
-   **Multiple Format Options**:
    -   **Video**: Download in `MP4`, `MKV`, `MOV`, or `AVI`.
    -   **Audio**: Extract audio-only streams to `MP3`, `FLAC`, `WAV`, or `M4A`.
-   **QuickTime Optimization**: The `MP4` option automatically re-encodes the video to the H.264 codec, ensuring perfect compatibility with QuickTime and other Apple devices.
-   **Real-time Progress Reporting**:
    -   A live progress bar tracks download percentage.
    -   The download button dynamically updates its text (`Downloading... 52%`).
    -   **Explicit FFmpeg Status**: Clearly indicates when `ffmpeg` is processing, merging, or re-encoding files so you know the app isn't frozen.
-   **Standalone & Portable**: Packaged into a single application that runs out of the box. **No need for users to install Python, `yt-dlp`, or `ffmpeg` manually.**

---

## 🚀 Getting Started

### Prerequisites

-   A computer running a modern version of **macOS** or **Windows**.

### Installation

1.  Go to the **[Releases](https://github.com/your-username/your-repo/releases)** page of this repository.
2.  Download the latest version for your operating system:
    -   **For macOS**: Download the `DataDrain.app.zip` file.
    -   **For Windows**: Download the `DataDrain.exe.zip` file.
3.  Unzip the file.
4.  Run the application!
    -   On macOS, you may need to **right-click** `DataDrain.app` and select **"Open"** the first time.

---

## 💻 How to Use

1.  **Paste** a YouTube video URL into the text box.
2.  Click the **Fetch (🔎)** button.
3.  **Select** your desired **Quality** and **Format** from the dropdown menus.
4.  Optionally, choose a different **Save To** location by clicking the **Browse (📁)** button.
5.  Click the **Download** button and watch the progress!

---

## 👨‍💻 For Developers: Building from Source

Interested in contributing or building the app yourself? Here’s how to get a development environment running.

### 1. Prerequisites

-   [Python 3.9+](https://www.python.org/)
-   `yt-dlp` (Command-line tool)
-   `ffmpeg` (Command-line tool)

**On macOS (via [Homebrew](https://brew.sh/)):**
```bash
brew install python yt-dlp ffmpeg
```
**On Windows (via [Chocolatey](https://chocolatey.org/) or [Scoop](https://scoop.sh/)):**
```bash
# Using Chocolatey
choco install python ffmpeg yt-dlp

# Using Scoop
scoop install python ffmpeg yt-dlp
```

### 2. Setup

```bash
# Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install the required Python libraries
pip install -r requirements.txt
```

*(You will need to create a `requirements.txt` file with the following content:)*
```txt
requests
Pillow
pyinstaller
```

### 3. Running the Script
With your virtual environment activated, simply run:
```bash
python3 youtube_downloader_pro_final.py
```

### 4. Packaging the Application

The final application is built using **PyInstaller**.

#### macOS Build (`.app`)

```bash
# 1. Build the app, bundling yt-dlp and ffmpeg
pyinstaller --name "DataDrain" \
            --windowed \
            --icon "icon.icns" \
            --add-binary "/opt/homebrew/bin/yt-dlp:." \
            --add-binary "/opt/homebrew/bin/ffmpeg:." \
            youtube_downloader_pro_final.py

# 2. Sign the app to fix the icon and ensure it's trusted
codesign --force --deep --sign - "dist/DataDrain.app"
```

#### Windows Build (`.exe`)

(Run these commands on a Windows machine)
```cmd
# Build the app (ensure yt-dlp.exe and ffmpeg.exe are in your system PATH)
pyinstaller --name "DataDrain" --windowed --icon "icon.ico" youtube_downloader_pro_final.py
```

---

## 🙏 Acknowledgments

This project would not be possible without the incredible work of the following open-source projects:

-   **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: For the core video downloading functionality.
-   **[FFmpeg](https://ffmpeg.org/)**: For all media processing, merging, and re-encoding.
-   **[PyInstaller](https://pyinstaller.org/)**: For packaging the script into a standalone application.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
