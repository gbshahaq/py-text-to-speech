import os


def delete_wav(prompt_path):
    wav_path = os.path.join(prompt_path + ".wav")
    mp3_path = os.path.join(prompt_path + ".mp3")

    if os.path.isfile(mp3_path) and os.path.isfile(wav_path):
        os.remove(wav_path)
