# Python script to read an Excel file and output mp3

File quality is tailored for use as telephony prompts

## Functionality split in separate .py files:
 - aws_tts_fn - generate file via AWS Polly
 - ms_tts_fn - generate file via MS Azure Speech
 - s3_upload - upload mp3 file from local machine to S3 bucket
 - wav_delete - separate script to delete redundant wav file after mp3 creation


## Additional Info
  Example file found in root Scripts folder ("Prompts-TTS.xlsx")

  Python requirements in requirements.txt
  Tested on Python 3.7

  Use boto3 for interacting with AWS
  Use azure.cognitiveservices.speech for interacting with Azure Speech
  Use pandas dataframe for elegance in data reading
  ~~Use pydub to convert Microsoft wav files - as 8khz mp3 cannot be generated~~

  **Use ffmpeg installed on local machine to handle the mp3 conversion of MS wav files - https://ffmpeg.org/**
  
  Use wav_delete to remove the wav file
  Use s3_upload to set content-type and upload mp3 file to corresponding language folder