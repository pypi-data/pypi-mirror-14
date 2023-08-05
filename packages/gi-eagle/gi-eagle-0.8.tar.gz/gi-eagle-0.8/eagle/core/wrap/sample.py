import numpy as np
import h5py
#from collections import namedtuple
from os.path import basename, splitext
from numpy.lib.recfunctions import merge_arrays, append_fields, stack_arrays

class Sample:
    def __init__(self, filename):
        self.filename = filename
        self.basename = basename(splitext(filename)[0])
        self.samplename = splitext(self.basename)[0]
        self.f = h5py.File(filename, 'r')


    def __meta__(self, path, name, default=b''):
        p = self.f
        if path:
            p = p[path]

        value = p.attrs.get(name, default)
        if type(value) == int:
            return value
        else:
            return value.decode()

    @property
    def disease(self):
        return self.__meta__("", "disease")

    @property
    def capturekit_coverage(self):
        return float(self.__meta__("variants", "capture_kit_coverage", 0))

    @property
    def chromosomes(self):
        return list(self.f["variants"].keys())

    def readcount(self, chrom):
        return int(self.f["variants"][chrom].attrs.get("readcount"))


    def duplication_rate(self):
        return float(self.__meta__("variants", "duplication_percentage", 0))


    def examined_pairs(self):
        return int(self.__meta__("variants", "examined_pairs", 0))


    def unmapped_reads(self):
        return int(self.__meta__("variants", "unmapped_reads", 0))


    def fields_view(self, arr, fields):
        dtype2 = np.dtype({name:arr.dtype.fields[name] for name in fields})
        return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)


    def position_to_key(self, pos):
        return (pos << 4)


    def encode_keys(self, chrom, variants):
        '''decode the key and append fields'''
        keys = variants["key"]
        positions = keys >> 4
        mask = (1 << 4) - 1
        types = np.bitwise_and(keys, mask) >> 1
        mask = 1
        het = np.bitwise_and(keys, mask)
        chroms = np.repeat(chrom, len(keys))
        m = merge_arrays((variants, chroms, positions, types, het), flatten=True)
        m.dtype.names= list(variants.dtype.names) + ["chrom", "position", "typ", "het"]
        return m
#        return append_fields(variants, ("chrom", "position", "typ", "het"), (chroms, positions, types, het))


    def keys(self, chrom):
#        print(self.basename, chrom)
        if not chrom in self.f["variants"]:
            return np.array([], dtype=np.int64)
        return self.f["variants"][chrom]["keys"][:]


    def variants(self,
        chrom,
        min_qual=0,
        effects=None,
        het=None,
        filter_dbs=[],
        unique=True,
        genes=[],
        fields=["key", "qual", "ref"],
        start=-1,
        stop=-1,
        decodekey=False,
        min_alt_mapping_qual=0,
        ):

        if not chrom in self.f["variants"]:
            return None
#            first_chrom = list(self.f["variants"])[0]
#            values = self.f["variants"][first_chrom]["values"][0:0]
#            return self.fields_view(values, fields)

        values = self.f["variants"][chrom]["values"][:]

        if start > -1 and stop > -1:
            start_index, stop_index = np.searchsorted(values["key"], (self.position_to_key(start), self.position_to_key(stop)))
            values = values[start_index:stop_index]

       # TODO: db option

        if values.shape[0] == 0:
            dtype_1 = self.f["variants"]["1"]["values"][:].dtype
            return self.fields_view(np.array([], dtype=dtype_1), fields)

        filter_crit = np.ones(len(values), dtype=np.bool)


        if "db" in self.f["variants"][chrom]:
            for filter_db in filter_dbs:
                db = self.f["variants"][chrom]["db"][filter_db]
                filter_crit &= np.logical_not(db)

        if min_qual:
            filter_crit &= values["qual"] > min_qual


        if min_alt_mapping_qual:
            filter_crit &= values["mq"] > min_alt_mapping_qual


        if effects:
            filter_crit &= (values["effect"] & effects) > 0

        if not het is None:
            filter_crit &= (values["key"] & 1) == het

        if len(genes):
            filter_crit &= np.in1d(values["gene_id"], np.array(genes))

        if len(fields) > 0:
            filtered_values = self.fields_view(values[filter_crit], fields)
        else:
            filtered_values = values[filter_crit]

        if unique:
            filtered_values = np.unique(filtered_values)

        # if decodekeys is True, decode all keys and append chrom, position, typ and het to the returned data, which is very expensive for huge lists
        if decodekey:
            filtered_values = self.encode_keys(chrom, filtered_values)

        return filtered_values


    def __repr__(self):
        return self.basename

    def __lt__(self, other):
        return self.basename < other.basename
