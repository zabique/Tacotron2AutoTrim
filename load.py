import re
import sys

from pydub import AudioSegment
from pydub.silence import split_on_silence

import glob
import os

import transcribe

file_number = 1

# assign files
input_file = 'input/' + sys.argv[1]

sound_file = AudioSegment.from_file(input_file)
sound_file = sound_file.set_frame_rate(22050)  # don't change this
sound_file = sound_file.set_channels(1)  # don't change this
audio_chunks = split_on_silence(sound_file, min_silence_len=750,  # 1000 cuts at 1 second of silence. 500 is 0.5 sec
                                silence_thresh=-40)

for i, chunk in enumerate(audio_chunks):

    if len(os.listdir('output/wavs')) == 0:
        print("Wavs directory is empty")
    else:
        list_of_files = glob.glob('output/wavs/*')  # * means all
        latest_file = max(list_of_files, key=os.path.getctime)

        # Extract numbers and cast them to int
        list_of_nums = re.findall('\\d+', latest_file)

        if int(list_of_nums[0]) >= file_number:
            file_number = int(list_of_nums[0]) + 1

    out_file = "output/wavs/{0}.wav".format(file_number)
    print("exporting", out_file)

    chunk.export(out_file, format="wav")

    transcription = transcribe.get_large_audio_transcription(out_file)

    if os.path.isfile('output/list.txt'):
        if os.stat("output/list.txt").st_size != 0:
            with open('output/list.txt', 'a+') as f:
                f.write(f'\nwavs/{file_number}.wav|' + transcription)
                f.flush()
        else:
            with open('output/list.txt', 'a+') as f:
                f.write(f'wavs/{file_number}.wav|' + transcription)
                f.flush()
    else:
        with open('output/list.txt', 'x') as f:
            f.write(f'wavs/{file_number}.wav|' + transcription)

    file_number = file_number + 1