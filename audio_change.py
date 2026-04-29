import os
import subprocess
import wave
import numpy as np
import struct
from pathlib import Path

# Professional standard: Constants in uppercase at the top
# Points to your local FFmpeg folder
FFMPEG_PATH = Path("ffmpeg") / "bin" / "ffmpeg.exe"

def mp3_to_voice_change(input_source: str, output_wav: str = None, pitch_factor: float = 0.75, speed_factor: float = 1.0) -> None:
    """
    Automates audio transformation using FFmpeg for streaming and NumPy for 
    digital signal processing (DSP).
    """
    # 1. Verification
    if not FFMPEG_PATH.exists():
        print(f"❌ FFmpeg missing at {FFMPEG_PATH}. Please check your installation.")
        return

    # 2. Setup File Names
    # If it's a URL, use a generic name; if it's a file, use the original name
    if input_source.startswith("http"):
        base_name = "streamed_output"
    else:
        base_name = Path(input_source).stem

    temp_wav = f"{base_name}_temp.wav"
    if output_wav is None:
        output_wav = f"{base_name}_processed.wav"

    print(f"🔄 Processing: {input_source} -> pitch={pitch_factor}, speed={speed_factor}x")

    # 3. Stream/Convert to WAV
    # We send the input_source directly to FFmpeg so URLs and local files both work
    cmd = [
        str(FFMPEG_PATH), "-y", "-i", input_source, 
        "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", temp_wav
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)

        # 4. Signal Processing (Original Core Logic)
        with wave.open(temp_wav, 'rb') as infile:
            params = infile.getparams()
            frames = infile.readframes(params.nframes)

        data = np.frombuffer(frames, np.int16).astype(np.float32) / 32768.0
        processed_channels = []

        for ch in range(params.nchannels):
            ch_data = data[ch::params.nchannels]

            # Speed Adjustment
            speed_len = int(len(ch_data) / speed_factor)
            speed_indices = np.linspace(0, len(ch_data) - 1, speed_len)
            sped_ch = np.interp(speed_indices, np.arange(len(ch_data)), ch_data)

            # Pitch Adjustment
            pitch_len = int(len(sped_ch) / pitch_factor)
            pitch_indices = np.linspace(0, len(sped_ch) - 1, pitch_len)
            shifted_ch = np.interp(pitch_indices, np.arange(len(sped_ch)), sped_ch)

            processed_channels.append(shifted_ch)

        # 5. Interleave and Pack
        final_data = np.empty((sum(len(ch) for ch in processed_channels),), np.float32)
        for i, ch_data in enumerate(processed_channels):
            final_data[i::params.nchannels] = ch_data

        final_data = np.clip(final_data * 32767, -32768, 32767).astype(np.int16)
        out_frames = struct.pack(f'{len(final_data)}h', *final_data)

        # 6. Save Final File
        new_params = params._replace(nframes=len(processed_channels[0]))
        with wave.open(output_wav, 'wb') as outf:
            outf.setparams(new_params)
            outf.writeframes(out_frames)

        print(f"✅ Process Complete: {os.path.abspath(output_wav)}")

    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg Error: {e.stderr}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
    finally:
        if os.path.exists(temp_wav):
            os.remove(temp_wav)

# Standard Entry Point - Essential for professional portfolios
if __name__ == "__main__":
    print("🎤 Professional Voice + Speed Changer")
    path_input = input("Enter MP3 path or URL: ").strip().strip('"')
    if path_input:
        mp3_to_voice_change(path_input, pitch_factor=0.75, speed_factor=1.5)