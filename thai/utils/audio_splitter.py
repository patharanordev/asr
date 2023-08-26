
from pydub import AudioSegment
import math

class SplitWavAudioMubin():
    def __init__(self, folder, filename, export_dir=None):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '\\' + filename
        self.audio = AudioSegment.from_wav(self.filepath)
        
        if export_dir is not None:
            self.export_dir = export_dir
        else:
            self.export_dir = folder
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename, seconds_per_clip=60):
        t1 = from_min * seconds_per_clip * 1000
        t2 = to_min * seconds_per_clip * 1000
        split_audio = self.audio[t1:t2]

        split_audio.export(self.export_dir + '\\' + split_filename, format="wav")
        
    def multiple_split(self, min_per_split, seconds_per_clip=60):
        total_mins = math.ceil(self.get_duration() / seconds_per_clip)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn, seconds_per_clip)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')
