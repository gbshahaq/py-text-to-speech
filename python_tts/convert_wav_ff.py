# for testing

import os
import sys
import subprocess
import shlex


base_path = 'c:/Temp/Test/en-GB_Sonia/'
mp3_path = os.path.join(base_path, 'AT_Thunderbirds.mp3')
wav_path = os.path.join(base_path, 'AT_Thunderbirds.wav')


command = shlex.split("ffmpeg -y -i " + wav_path + ' -vn -ar 8000 -ac 1 -b:a 32k ' + mp3_path)
subprocess.run(command)
