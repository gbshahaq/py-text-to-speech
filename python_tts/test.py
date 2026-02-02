import ms_tts_fn as ms
import aws_tts_fn as aws
import wav_delete

import os

provider = 'MS'    # AWS or MS
lang = 'cs-CZ'      # ISO lang-ISO country
voice = 'Vlasta'      # just the name of the voice ID per the provider
voice_folder = lang + '_' + voice
text = 'Takže z jakého důvodu dnes voláte?'
ms_voice = lang + '-' + voice + 'Neural'
aws_voice = voice
#TARGET_DIR = os.path.join('C:','Temp','Test')
TARGET_DIR = 'C:/Temp/Test/'
prompt = 'AT_INTENT'


if(provider == 'MS'):
    ms.tts(voice_folder,ms_voice,text,TARGET_DIR,prompt)
    prompt_path = os.path.join(TARGET_DIR,voice_folder,prompt)
    wav_delete.delete_wav(prompt_path)
elif(provider == 'AWS'):
    aws.tts(voice_folder,aws_voice,text,TARGET_DIR,prompt)

print(voice_folder + '/' + prompt + '.mp3 : generated ok')