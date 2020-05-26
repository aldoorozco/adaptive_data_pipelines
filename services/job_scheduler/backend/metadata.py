from os import listdir
from os.path import isfile, getsize, join
from collections import Counter

class Metadata:
    def __init__(self, filepath):
        # Get all files in the filepath
        self.files = [join(filepath, f) for f in listdir(filepath) if isfile(join(filepath, f))]

        # Get the total size of all files combined
        sizes = [getsize(f) for f in self.files]
        self.size = sum(sizes)

        # Get the most common data set extension
        cntr = Counter([f.split('.')[1] for f in self.files])
        sorted_extensions = {k: v for k, v in sorted(cntr.items(), key=lambda item: item[1])}
        self.source_type = list(sorted_extensions.keys())[0]
