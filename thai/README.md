# Y2T

For converting YouTube-to-text (video > audio > text).

## Preparation

- Create `audios` directory.
- Create your `env` by `python -m venv env` then active it.
- Adding your video into `data/{PROJECT_NAME}/video` directory, your project directory structure should look like this:

```txt
.
├───data
│   ├───{PROJECT_NAME}
│   │   ├───audios
│   │   ├───tmp
│   │   └───videos
│   │       └───{EXEC_DATETIME_FORMAT}.mp4
|   └───convertTo16Hz.ps1
├───result
│   └───{PROJECT_NAME}
│       └───{EXEC_DATETIME_FORMAT}
└───thai
    ├───env
    │   └───...
    ├───requirements.txt
    ├───run.py
    └───utils
        └───audio_splitter.py
```

- Install torch to support your GPU, in this case I using CUDA 12.1 :

```sh
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
```

- Install dependencies :

```sh
pip install -r requirements.txt
```

## Convert `.mp4` to `.wav`

In `data` directory, run `ffmpeg` for converting `.mp4` to `.wav` :

```sh
ffmpeg -i ./{PROJECT_NAME}/videos/{PROJECT_NAME}.mp4 -acodec pcm_s16le -ac 1 -ar 16000 ./{PROJECT_NAME}/audios/{PROJECT_NAME}.wav
```

## Thai language

Before you run `run.py`, please ensure your GPU memory enough for inferencing or not.

In case you got error message similar below message :

> torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 1.59 GiB. GPU 0 has a total capacty of 15.99 GiB of which 0 bytes is free. Of the allocated memory 20.12 GiB is allocated by PyTorch, and 134.00 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF

Please set `max_split_size_mb` to `PYTORCH_CUDA_ALLOC_CONF`, example :

```python
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"
```

Or try to trim or split out your video to be multi-parts :

```python
# ...

split_wav = SplitWavAudioMubin(folder=folder, filename=filename, export_dir=export_dir)
split_wav.multiple_split(min_per_split=1, seconds_per_clip=30)
```

**Note**: `SplitWavAudioMubin` class is in `thai/utils/audio_splitter.py` file.

then run command below separatly:

```sh
python run.py
```

The output or text result will be wrote into `result/{PROJECT_NAME}/{EXEC_DATETIME_FORMAT}/{PROJECT_NAME}.txt`.
