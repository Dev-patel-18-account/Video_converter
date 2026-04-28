import os
import subprocess
import wave
import numpy as np
import struct
from pathlib import Path

def mp3_to_voice_change(input_mp3, output_wav=None, pitch_factor=0.75, speed_factor=1.0):
    """
    Converts MP3 to WAV and applies pitch/speed shifts using numpy resampling.
    """
    input_path = Path(input_mp3)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Source file not found: {input_mp3}")

    # Setup file names professionally
    base_name = input_path.stem
    temp_wav = f"{base_name}_temp.wav"
    if output_wav is None:
        output_wav = f"{base_name}_processed.wav"

    print(f"🔄 Processing: {input_path.name}")
    
    try:
        # Step 1: MP3 → WAV using system FFmpeg
        # Using 'ffmpeg' directly assumes it is installed on the system path
        subprocess.run([
            "ffmpeg", "-y", "-i", str(input_path), 
            "-vn", "-acodec", "pcm_s16le", 
            "-ar", "44100", "-ac", "2", temp_wav
        ], capture_output=True, check=True)
        
        # Step 2: Audio Signal Processing
        with wave.open(temp_wav, 'rb') as infile:
            params = infile.getparams()
            frames = infile.readframes(params.nframes)
        
        data = np.frombuffer(frames, np.int16).astype(np.float32) / 32768.0
        shifted_channels = []
        
        for ch in range(params.nchannels):
            ch_data = data[ch::params.nchannels]
            
            # Speed manipulation
            speed_len = int(len(ch_data) / speed_factor)
            speed_indices = np.linspace(0, len(ch_data)-1, speed_len)
            sped_ch = np.interp(speed_indices, np.arange(len(ch_data)), ch_data)
            
            # Pitch manipulation
            pitch_len = int(len(sped_ch) / pitch_factor)
            pitch_indices = np.linspace(0, len(sped_ch)-1, pitch_len)
            shifted_ch = np.interp(pitch_indices, np.arange(len(sped_ch)), sped_ch)
            
            shifted_channels.append(shifted_ch)
        
        # Interleave channels
        shifted = np.empty((sum(len(ch) for ch in shifted_channels),), np.float32)
        for i, ch_data in enumerate(shifted_channels):
            shifted[i::params.nchannels] = ch_data
        
        # Convert back to 16-bit PCM
        shifted = np.clip(shifted * 32767, -32768, 32767).astype(np.int16)
        out_frames = struct.pack(f'{len(shifted)}h', *shifted)
        
        # Step 3: Write Final File
        new_params = params._replace(nframes=len(shifted_channels[0]))
        with wave.open(output_wav, 'wb') as outf:
            outf.setparams(new_params)
            outf.writeframes(out_frames)
            
        print(f"✅ Success! Saved to: {os.path.abspath(output_wav)}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        if os.path.exists(temp_wav):
            os.remove(temp_wav)

if __name__ == "__main__":
    print("🎤 Professional Voice + Speed Changer")
    path_input = input("Enter MP3 path: ").strip().strip('"')
    if path_input:
        mp3_to_voice_change(path_input, pitch_factor=0.75, speed_factor=1.5)