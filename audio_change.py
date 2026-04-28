import sys
import os
import subprocess
import wave
import numpy as np
import struct

ffmpeg_path = os.path.join("ffmpeg", "bin", "ffmpeg.exe")

def mp3_to_voice_change(input_mp3, output_wav=None, pitch_factor=0.75, speed_factor=1.0):
    if not os.path.exists(ffmpeg_path) or not os.path.exists(input_mp3):
        print("❌ FFmpeg/MP3 missing")
        return
    
    base_name = os.path.splitext(os.path.basename(input_mp3))[0]
    temp_wav = f"{base_name}_temp.wav"
    if output_wav is None:
        output_wav = f"{base_name}_male_fast.wav"
    
    print(f"🔄 {os.path.basename(input_mp3)} → pitch={pitch_factor}, speed={speed_factor}x")
    
    # MP3 → WAV
    cmd = [ffmpeg_path, "-y", "-i", input_mp3, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", temp_wav]
    subprocess.run(cmd, capture_output=True, text=True, check=True)
    
    # Process
    with wave.open(temp_wav, 'rb') as infile:
        params = infile.getparams()
        frames = infile.readframes(params.nframes)
    
    data = np.frombuffer(frames, np.int16).astype(np.float32) / 32768
    
    # Channel loop (stereo safe)
    shifted_channels = []
    for ch in range(params.nchannels):
        ch_data = data[ch::params.nchannels]
        
        # COMBINED: speed then pitch
        # Speed: resample (shorter for faster)
        speed_len = int(len(ch_data) / speed_factor)
        speed_indices = np.linspace(0, len(ch_data)-1, speed_len)
        sped_ch = np.interp(speed_indices, np.arange(len(ch_data)), ch_data)
        
        # Pitch: resample sped (shorter for lower pitch)
        pitch_len = int(len(sped_ch) / pitch_factor)
        pitch_indices = np.linspace(0, len(sped_ch)-1, pitch_len)
        shifted_ch = np.interp(pitch_indices, np.arange(len(sped_ch)), sped_ch)
        
        shifted_channels.append(shifted_ch)
    
    # Interleave
    shifted = np.empty((sum(len(ch) for ch in shifted_channels),), np.float32)
    for i, ch_data in enumerate(shifted_channels):
        shifted[i::params.nchannels] = ch_data
    
    shifted = np.clip(shifted * 32767, -32768, 32767).astype(np.int16)
    out_frames = struct.pack(f'{len(shifted)}h', *shifted)
    
    new_nframes = len(shifted_channels[0])
    new_params = params._replace(nframes=new_nframes)
    
    with wave.open(output_wav, 'wb') as outf:
        outf.setparams(new_params)
        outf.writeframes(out_frames)
    
    os.remove(temp_wav)
    print(f"✅ {os.path.abspath(output_wav)}")

# Run
print("🎤 Voice + Speed Changer")
input_mp3 = input("MP3 path: ").strip().strip('"')
mp3_to_voice_change(input_mp3, pitch_factor=0.75, speed_factor=1.5)  # FASTER + DEEPER