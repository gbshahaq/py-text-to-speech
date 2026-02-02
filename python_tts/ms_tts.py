# for unit testing

import os
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
import subprocess

wav_path="c:/Temp/TTS/testfile4.wav"
mp3_path = "c:/Temp/TTS/testfile4.mp3"
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
# audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
audio_config = speechsdk.audio.AudioOutputConfig(filename=wav_path)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Get text from the console and synthesize to the default speaker.
print("Enter some text that you want to speak >")
text = input()

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
# speech_synt_file = speech_synt_file

audio = AudioSegment.from_wav(wav_path)
audio = audio.set_frame_rate(8000)
audio.export(mp3_path, format="mp3")

# try deleting wav file after mp3 conversion

if os.path.isfile(mp3_path):
    os.chdir('c:/')
    os.remove(wav_path)

    
if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")