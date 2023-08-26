import os
import shutil
import datetime
import torch
from pythaiasr import asr
from utils.audio_splitter import SplitWavAudioMubin

data_dir = '../data'
result_dir = '../result'
project_name = 'healty-time'
execute_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
temp_folder = f'{data_dir}/{project_name}/tmp'
audio_folder = f'{data_dir}/{project_name}/audios'
output_folder = f'{result_dir}/{project_name}/{execute_date}'
file = f'{data_dir}/{project_name}/videos/{project_name}.wav'
model = 'wannaphong/wav2vec2-large-xlsr-53-th-cv8-deepcut'

def split_audio(folder:str, filename:str, export_dir:str=None):
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)

    os.mkdir(export_dir)

    split_wav = SplitWavAudioMubin(folder=folder, filename=filename, export_dir=export_dir)
    split_wav.multiple_split(min_per_split=1, seconds_per_clip=30)

def speech_to_text(model:str, audio_fpath:str, output_folder:str, ori_fname:str):
        
    print(f'[*] processing audio file : {audio_fpath}...')

    torch.cuda.empty_cache()
    result = asr(data=audio_fpath, model=model, sampling_rate=16_000)
    print(result)

    output_fpath = f'{output_folder}/{os.path.splitext(ori_fname)[0]}.txt'
    with open(output_fpath, encoding='utf-8', mode='a+') as f:
        f.write(result)


if __name__ == '__main__':

    # # Firstly got None
    # print(os.getenv('PYTORCH_CUDA_ALLOC_CONF'))

    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'
    print(f'PYTORCH_CUDA_ALLOC_CONF : {os.getenv("PYTORCH_CUDA_ALLOC_CONF")}')

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for fname in os.listdir(audio_folder):
        split_audio(audio_folder, fname, temp_folder)
        for wavfile in os.listdir(temp_folder):
            speech_to_text(model, f'{temp_folder}/{wavfile}', output_folder, fname)
            
    torch.cuda.empty_cache()
    del os.environ['PYTORCH_CUDA_ALLOC_CONF']