import os

import aws_tts_fn as aws
import ms_tts_fn as ms
import wav_delete

# declare variables and fill in required values


provider = "Microsoft"  # "Microsoft" or "Amazon"
voice = "Bella"  # or "Matthew" or "Joanna" or "Brian" or "Amy"

# Amazon voices: https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
# Microsoft voices: https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#text-to-speech
# use only the voice "name" - not the full voice id eg. "Klarissa" and not "de-DE-KlarissaNeural"

text = "Hi, I'm Sarah, the BuildingFun Customer service virtual assistant!"

prompt = "AT_1"  # this is the name of the file to be generated
lang = "en-GB"  # or "en-US" or "fr-FR" or "de-DE" or "es-ES" or "it-IT" or "ja-JP" or "ko-KR" or "pt-BR" or "ro-RO" or "cmn-CN" or "zh-HK" or "zh-TW"

# NB some language codes are different to those used elsewhere - eg. nb-NO (Norwegian) and

# set git project voice_files directory as local target
os.chdir(".")
curr_dir = os.getcwd()
TARGET_DIR = os.path.join(curr_dir, "voice_files", "TTS")

if provider == "Microsoft":
    voice_folder = lang + "_" + voice
    voice_id = lang + "-" + voice + "Neural"
    ms.tts(voice_folder, voice_id, text, TARGET_DIR, prompt)
    prompt_path = os.path.join(voice_folder, prompt)
    wav_delete.delete_wav(prompt_path)
    print(lang + "_" + voice + "_" + prompt + ": generated ok")
elif provider == "Amazon":
    voice_folder = lang + "_" + voice
    aws.tts(voice_folder, voice, text, TARGET_DIR, prompt, "standard")
    prompt_path = os.path.join(voice, prompt)
    print(lang + "_" + voice + "_" + prompt + ": generated ok")
else:
    print("Provider not recognised")
