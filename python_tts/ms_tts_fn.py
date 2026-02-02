import os
import azure.cognitiveservices.speech as speechsdk
import s3_upload as s3
import logging
import subprocess
import shlex


def tts(voice_folder, voice, prompt_text, folderpath, fname):
    
    # BUCKET = 's3-dev-prompts'
    BUCKET = "s3-ivr-digital-files"

    lang_path = os.path.join(folderpath, voice_folder)
    lang_path_exists = os.path.exists(lang_path)
    if not lang_path_exists:
        os.makedirs(lang_path)

    wav_path = os.path.join(lang_path, fname + ".wav")
    mp3_path = os.path.join(lang_path, fname + ".mp3")


    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get("SPEECH_KEY"),
        region=os.environ.get("SPEECH_REGION"),
    )
    # audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=wav_path)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = voice

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    speech_synthesis_result = speech_synthesizer.speak_text_async(prompt_text).get()

    """
    # convert to mp3 using pydub
    # does a terrible job of conversion - no way to set required parameters
    # use ffmpeg directly
    
    audio = AudioSegment.from_wav(wav_path)
    audio = audio.set_frame_rate(8000)
    audio = audio.set_bit_rate(32)
    audio.export(mp3_path, format="mp3")

#    audio = AudioSegment.from_file(wav_path, format="raw", frame_rate=8000, channels=1, sample_width=2) # 8kHz, mono, 16-bit
#    audio.export(mp3_path, format="mp3")      
    """
    # due to calling a command directly, enforce Windows-specific pathing
    wav_path_cmd = wav_path.replace("\\", "/")
    mp3_path_cmd = mp3_path.replace("\\", "/")

    # calling ffmpeg on local machine directly
    # for lambda-ising - ffmpeg conversion is available as an off-the-shelf pre-built
    # parameters below specify 8kHz frame rate (-ar), mono channel (-ac 1), 32kbps bit rate (-b:a)
    command = shlex.split(
        "ffmpeg -y -i " + wav_path_cmd + " -vn -ar 8000 -ac 1 -b:a 32k " + mp3_path_cmd
    )
    subprocess.run(command)

    # upload mp3 to s3
    bucket_loc = voice_folder + "/" + fname + ".mp3"
    s3.upload_file(mp3_path, BUCKET, bucket_loc)

    if (
        speech_synthesis_result.reason
        == speechsdk.ResultReason.SynthesizingAudioCompleted
    ):
        result = "Speech synthesized for text [{}]".format(prompt_text)
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        result = "Speech synthesis cancelled: {}".format(cancellation_details.reason)
        logging.exception(result)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                result = "Error details: {}".format(cancellation_details.error_details)
                logging.exception(result)
    #                print("Did you set the speech resource key and region values?")

    return result
