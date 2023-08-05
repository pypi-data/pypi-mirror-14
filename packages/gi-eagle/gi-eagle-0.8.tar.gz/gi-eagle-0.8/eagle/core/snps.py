import os
import h5py, sys
import numpy as np
from collections import defaultdict
import argparse
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from collections import namedtuple
import json
from urllib.request import Request, urlopen
from itertools import islice
from eagle.core.effectenum import Effect, exon_effects
from eagle.core.wrap.sample import Sample
from numpy.lib.recfunctions import append_fields, stack_arrays


Config = namedtuple("Config", "effects min_qual min_samples_per_gene min_samples_per_variant min_variants_per_gene genes ignore_heterozygosity filter_dbs min_alt_mapping_qual")


class NamedDict(dict):
    def __init__(self, *args, **kwargs):
        super(NamedDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

        self.samples = set()
        self.symbols = set()
        self.effect = 0
        self.maxqual = 0
        self.heterozygot = 0
        self.minaf = 1.0
        self.maxaf = 0.0
        self.maximpact = 0


def encode_keys(variants):
    '''decode the key and append fields'''
    keys = variants["key"]
    position = keys >> 4
    typ = keys >> 1 & 7
    het = keys & 1
    ret = append_fields(variants, data=(position, typ, het), names=("position", "typ", "het"))
    return ret
#    return position, typ, het, variants


def fields_view(arr, fields):
    dtype2 = np.dtype({name:arr.dtype.fields[name] for name in fields})
    return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)


def filtered(chrom, case, x):
    t_data, b_data, config = x
    # building the filtering list

    # build the filter containing of all control samples and the information from the group datas
    if b_data:
        keys_control = np.unique(np.concatenate(b_data))
    else:
        keys_control = np.array([], dtype=np.int64)

    d = defaultdict(lambda: NamedDict()) # stores the samples


    remaining = []

    #for each case
    for i, values in enumerate(t_data):
        if values is None:
            continue
        keys = values["key"]

        if config.ignore_heterozygosity:
            # TODO: replace astype with default int64
            remaining = values[np.in1d(keys.astype(np.int64)>>1, keys_control.astype(np.int64)>>1, invert=True)]
        else:
            remaining = values[np.in1d(keys, keys_control, invert=True)]

        for r in encode_keys(remaining):
            key = r["key"]
            item = d[key]
            item.key = key
            item.chrom = chrom
            item.typ = r["typ"]
            item.position = r["position"]
            item.samples.add(case[i].basename)
            item.symbols.add(r["gene_id"])
            item.effect |= r["effect"]
            item.maxqual = int(max(item.maxqual, r["qual"]))
            item.heterozygot |= 1 if r["typ"] else 2
            item.ref = chr(r["ref"])
            item.context = r["context"]
            item.mq = r["mq"]
            item.minaf = min(item.minaf, r["alt_count"] / r["depth"])
            item.maxaf = max(item.maxaf, r["alt_count"] / r["depth"])
            item.maximpact = max(item.maximpact, r["impact"])

    #filter min samples per variant and min variants per gene
    ret = [v for v in d.values() if len(v.samples) >= config.min_samples_per_variant]

    return ret


def opendata(chrom, case, control, config):
    #list the names of the case samples
    case_names = [s.samplename.encode() for s in case]
#    print(np.in1d(control_names, control_groups[0].samples))

    #list all variants of all case samples
    case_variants = [s.variants(chrom=chrom, filter_dbs=config.filter_dbs, min_qual=config.min_qual, fields=[], effects=config.effects, genes=config.genes, min_alt_mapping_qual=config.min_alt_mapping_qual) for s in case]
    control_keys = [s.keys(chrom) for s in control]

    return case_variants, control_keys, config


def run(case,
    control,
    effects=0,
    min_qual=50,
    min_samples_per_gene=1,
    min_samples_per_variant=1,
    min_variants_per_gene=1,
    genes=[],
    ignore_heterozygosity=True,
    db=[],
    min_alt_mapping_qual=0,
    ):

    config = Config(
        effects,
        min_qual,
        min_samples_per_gene,
        min_samples_per_variant,
        min_variants_per_gene,
        [g.encode() for g in genes],
        ignore_heterozygosity,
        filter_dbs=db,
        min_alt_mapping_qual=min_alt_mapping_qual,
    )

    case = [Sample(c) for c in case]
    control = [Sample(c) for c in control]

    #get chromosomes
    chromosomes = []
    for c in case:
        chromosomes.extend(c.chromosomes)
    chromosomes = list(set(chromosomes))


    ret = []

    for chrom in chromosomes:
        records = filtered(chrom, case, opendata(chrom, case, control, config))

        # filter minimum samples per gene and minimum variants per gene
        samples_per_gene = defaultdict(set)
        variants_per_gene = defaultdict(set)

        for item in records:
            for gene in item.symbols:
                samples_per_gene[gene] |= item.samples
                variants_per_gene[gene].add((item.chrom, item.position))
                item.common = samples_per_gene[gene]
                item.variants_per_gene = variants_per_gene[gene]

        records_filtered = [r for r in records if len(r.common) >= min_samples_per_gene and len(r.variants_per_gene) >= config.min_variants_per_gene]
        ret.extend(sorted(records_filtered, key=lambda r: (r.chrom, r.position)))

    return ret


def out(x):
    for i in x:
        print(*sorted(map(lambda x: x.decode(), i.symbols)), sep=",", end="\t")
        print(*sorted(i.samples), sep=",", end="\t")
        print(i.chrom, i.position, i.ref, "ACGT    "[i.typ], i.context.decode(), i.mq)


def main(args):
    effects = 131072 # TODO: change this (only missense)
    if not args.db:
        args.db = []
    out(run(case=args.case, control=args.control, db=args.db, effects=effects, min_qual=int(args.minqual), min_alt_mapping_qual=int(args.minaltmq)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", nargs="+")
    parser.add_argument("--control", nargs="+")
    parser.add_argument("--db", nargs="*")
    parser.add_argument("--minqual", default=0)
    parser.add_argument("--minaltmq", default=0)
    args = parser.parse_args()

    main(args)
