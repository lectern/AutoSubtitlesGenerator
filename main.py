import whisperx
import os, sys
from datetime import timedelta

# https://stackoverflow.com/a/45669280/20218615
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

class Subtitles:

    delay = 0.3

    def group_text(self, words, length):
        grouped = []
        split_index = []
        new_index = []

        if (length >= len(words)):
                return words
        
        # seperate by punctuation
        for i in range(len(words) - 1):
            a, b = words[i], words[i+1]
            delta_t = float(b['start']) - float(a['end'])
            if (a['text'][-1] in ['.', '!', '?', ','] or (delta_t > self.delay)):
                split_index += [i + 1]
        
        # seperate by delay
        if 0 not in split_index:
            split_index += [0]
        if len(words) not in split_index:
            split_index += [len(words)]
        
        # get filler index to fix long word groups
        for i in range(len(split_index) - 1):
            if (split_index[i + 1] - split_index[i] >= length):
                new_index = [x for x in range(split_index[i], split_index[i + 1], length)]

            split_index += new_index[1:]
        split_index.sort()
        split_index = split_index[1:-1]

        # group words together
        # https://stackoverflow.com/a/1198876/20218615
        grouped = [words[i:j] for i, j in zip([0]+split_index, split_index+[None])]
        grouped = list(filter(None, grouped))
        return grouped

    def gen_srt(self, path, grouped):
        with open(path + ".srt", "a", encoding="utf-8") as f:
            for group in grouped:
                sub_index = grouped.index(group) + 1
                word_group = []

                # calculate start and end utterance
                start_time = float(group[0]['start'])
                start_format = "{:0>8}".format(str(timedelta(seconds=int(start_time))))
                start_milli = int(1000 * (start_time - int(start_time)))

                end_time = float(group[-1]['end'])
                end_format = "{:0>8}".format(str(timedelta(seconds=int(end_time))))
                end_milli = int(1000 * (end_time - int(end_time)))
                
                for word in group:
                    word_group += [word['text']]

                f.write(f"{sub_index}\n")
                f.write(f"{start_format},{start_milli:03} --> {end_format},{end_milli:03}\n")
                f.write(" ".join(word_group) + "\n" * 2)

if __name__ == "__main__":
    length = -1
    delay = 0.

    device = "cuda" 
    audio_file = input("file path (video|audio): ")

    while delay <= 0:
        try:
            delay = float(input("no sound filter delay: "))
            if delay <= 0:
                print("<err> only integers of value greater than 0.")
        except:
            print("<err> only integers of value greater than 0.")

    while length <= 0:
        try:
            length = int(input("max number of words per subtitle: "))
            if length <= 0:
                print("<err> only integers of value greater than 0.")
        except:
            print("<err> only integers of value greater than 0.")

    sub_track = Subtitles()
    sub_track.delay = delay

    # transcribe with original whisper
    model = whisperx.load_model("small.en", device)
    result = model.transcribe(audio_file)

    # load alignment model and metadata
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)

    # align whisper output
    with HiddenPrints():
        result_aligned = whisperx.align(result["segments"], model_a, metadata, audio_file, device)
    
    # group the words
    grouped = Subtitles.group_text(sub_track, result_aligned["word_segments"], length)

    # generate subtitles
    Subtitles.gen_srt(sub_track, audio_file, grouped)