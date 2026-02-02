from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import s3_upload as s3
import logging


def tts(voice_folder, voice, prompt_text, folderpath, fname, engine = "neural"):
    # Create a client using the credentials and region defined in the [PollyService]
    # section of the AWS credentials file (~/.aws/credentials).
    # BUCKET = 's3-dev-prompts'
    
    
    BUCKET = "s3-ivr-digital-files"
    session = Session(profile_name="PollyService")
    polly = session.client("polly")

    lang_path = os.path.join(folderpath, voice_folder)
    lang_path_exists = os.path.exists(lang_path)
    if not lang_path_exists:
        os.makedirs(lang_path)

    mp3_path = os.path.join(lang_path, fname + ".mp3")

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(
            Text=prompt_text,
            OutputFormat="mp3",
            SampleRate="8000",
            VoiceId=voice,
            Engine=engine,
        )

    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        result = error
        logging.exception(result)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            #           output = os.path.join(gettempdir(), "speech.mp3")
            output = mp3_path
            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
                    result = "audio output ok"

            except IOError as error:
                # Could not write to file, exit gracefully
                result = error
                logging.exception(result)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        result = "Could not stream audio"
        logging.exception(result)
        sys.exit(-1)

    bucket_loc = voice_folder + "/" + fname + ".mp3"
    # upload mp3 to s3
    s3.upload_file(mp3_path, BUCKET, bucket_loc)

    return result
