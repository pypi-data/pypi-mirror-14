import numpy as np
import h5py
#from collections import namedtuple
from os.path import basename, splitext

class Group:
    def __init__(self, filename):
        self.filename = filename
        self.basename = basename(splitext(filename)[0])
        self.f = h5py.File(filename, 'r')


#    def fields_view(self, arr, fields):
#        dtype2 = np.dtype({name:arr.dtype.fields[name] for name in fields})
#        return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)

    @property
    def samples(self):
        return self.f["samples"][:]


    def chromosomes(self):
        return [c for c in self.f["snps"]]


    def variants(self, chrom):
        return self.f["variants"][chrom]["values"][:]


    def __repr__(self):
        return self.basename


    def __lt__(self, other):
        return self.basename < other.basename
