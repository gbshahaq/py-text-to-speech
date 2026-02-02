#for testing

from pydub import AudioSegment


def convert_wav(wav_path, mp3_path):

    audio = AudioSegment.from_file(wav_path, format="raw", frame_rate=8000, channels=1, sample_width=2) # 8kHz, mono, 16-bit
    audio.export(mp3_path, format="mp3")
        
    
