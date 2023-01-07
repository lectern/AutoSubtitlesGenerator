# Auto Subtitles Generator

## What is this?
Auto generate subtitles (.srt) given a video or audio file using [WhispherX](https://github.com/m-bain/whisperX). Essentially, it takes the generated word-level timestamps and formats them according to user specifications and sentence recognization.

## Demo:
https://youtu.be/Oh1WU_MHpYk
[![Screenshot_1](https://user-images.githubusercontent.com/30962319/211169733-d43586b0-e810-4527-8fe4-8b2885f87c2e.png)](https://youtu.be/Oh1WU_MHpYk)


## Download and Installation
If you wish to download and install this:

You must first install WhispherX:
```
$ pip install git+https://github.com/m-bain/whisperx.git
```

or if WhisperX is already installed:
```
$ pip install git+https://github.com/m-bain/whisperx.git --upgrade
```
You may also need to install FFMPEG, Rust etc. Follow OpenAI's instructions here https://github.com/openai/whisper#setup.

Next, download the auto subtitles generator:
```
$ git clone https://github.com/lectern/auto_subtitles_generator.git
$ cd auto_subtitles_generator
$ python main.py
```

Note that in some cases, CUDA will not be installed with Torch. In which case you should do the following if you have a supported GPU:
```
$ pip uninstall torch
$ pip cache purge
$ pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
```

## Usage:
You will be prompted with 3 inputs:
1. file path (video|audio): **relative or complete file path for any supported filetype which can be found by performing `ffmpeg -formats`**
2. no sound filter delay: **the amount of no speech delay between words to consider as a pause (int > 0)**
3. max number of words per subtitle: **the maximum number of words per each subtitle (int > 0)**

Once all inputs are valid and set, a .srt file will be found in the same location as your video once the processing is done.

Feel free to contact me @ Lectern#5112 if any problems arise.
