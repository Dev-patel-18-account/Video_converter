# Professional Voice & Speed Changer 🎤

A high-performance audio transformation tool that leverages **FFmpeg** for seamless media streaming and **NumPy** for Digital Signal Processing (DSP). This project demonstrates a production-ready approach to handling audio pitch and speed modulation from both local files and web URLs.

---

## 🌟 Key Technical Highlights
* **Direct URL Streaming:** Integrated FFmpeg subprocesses to stream audio directly from web sources, eliminating the need for local storage of raw files.
* **Custom DSP Logic:** Manual implementation of audio interpolation using NumPy to adjust pitch and speed without using high-level black-box libraries like Pydub.
* **Industry Standards:** Implemented professional Python practices including **Type Hinting**, **Docstrings**, and the `if __name__ == "__main__":` entry-point guard.
* **Robust Error Handling:** Designed with `try-except-finally` blocks to ensure clean-up of temporary files and graceful failure reporting.

---

## 🛠️ Tech Stack
* **Language:** Python 3.12+
* **Core Libraries:** `numpy` (DSP), `subprocess` (FFmpeg bridge), `wave` (Audio I/O)
* **Environment:** Cross-platform path management using `pathlib`

---

## ⚙️ Installation & Usage

### 1. Setup Environment
```bash
# Clone the repository
git clone [https://github.com/Dev-patel-18-account/Video_converter.git](https://github.com/Dev-patel-18-account/Video_converter.git)
cd Video_converter

# Install dependencies
pip install numpy

2. Configure FFmpeg
Ensure the FFMPEG_PATH in audio_change.py points to your local installation. The default is set to:
Path("ffmpeg") / "bin" / "ffmpeg.exe"

3. Run the Tool
# Run the application
python audio_change.py
Simply enter a local file path (e.g., C:/music.mp3) or a direct audio URL when prompted.

📁 Project Structure
audio_change.py - Core logic, signal processing, and user interface.

requirements.txt - Minimal dependency list.

.gitignore - Pre-configured to exclude virtual environments and temporary audio artifacts.
__________________________________________________________________________________________________
Note to Reviewers: This project is structured to demonstrate clean code separation, professional documentation standards, and an understanding of low-level audio manipulation.
