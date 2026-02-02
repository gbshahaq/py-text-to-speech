"""
Read an Excel file of prompt data and generate an mp3 to be stored on local machine
Store in a S3 bucket

Python prerequisites listed in requirements.txt
Tested on Python 3.7
Example Excel sheet is in the root Scripts folder

"""
# pip install -r requirements.txt
import os

import aws_tts_fn as aws
import ms_tts_fn as ms
import pandas as pd
import wav_delete

# xl_file = 'C:\Users\Me\Prompts-TTS.xlsx'
xl_sheet = "BELLA"

# read the columns required from the source sheet and in to a pandas dataframe
df = pd.read_excel(
    r"C:\Users\Me\Prompts-TTS.xlsx",
    sheet_name=xl_sheet,
    usecols=["Prompt", "LanguageCode", "Provider", "VoiceId", "N/S", "TEXT"],
)

# set git project voice_files directory as local target
os.chdir(".")
curr_dir = os.getcwd()
TARGET_DIR = os.path.join(curr_dir, "voice_files", "TTS")


# declare empty variables
voice = ""
text = ""
prompt = ""

# instantiate 2 dataframes - one for MS processing, one for AWS
# this helpfully ignores any blank rows
# using df.loc is apparently less expensive than alternatives - and still simple to understand syntax

df_ms = df.loc[df["Provider"] == "Microsoft"]
df_aws = df.loc[df["Provider"] == "Amazon"]

# loop through MS results
for row in df_ms.itertuples(index=True):
    voice_id = getattr(row, "VoiceId")
    voice = (
        getattr(row, "LanguageCode") + "-" + voice_id + "Neural"
    )  # MS voice ids are more detailed than a name
    text = getattr(row, "TEXT")
    prompt = getattr(row, "Prompt")
    lang = getattr(row, "LanguageCode")
    voice_folder = lang + "_" + voice_id

    ms.tts(voice_folder, voice, text, TARGET_DIR, prompt)
    prompt_path = os.path.join(TARGET_DIR, voice_folder, prompt)
    wav_delete.delete_wav(prompt_path)
    print(lang + "_" + voice_id + "_" + prompt + ": generated ok")


# loop through AWS results
for row in df_aws.itertuples(index=True):
    voice = getattr(row, "VoiceId")
    text = getattr(row, "TEXT")
    prompt = getattr(row, "Prompt")
    lang = getattr(row, "LanguageCode")
    voice_folder = lang + "_" + voice

    aws.tts(voice_folder, voice, text, TARGET_DIR, prompt)
    print(lang + "_" + voice + "_" + prompt + ": generated ok")
