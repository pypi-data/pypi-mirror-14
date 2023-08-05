import h5py
import argparse
import numpy as np

from collections import namedtuple, defaultdict
from eagle.core.wrap.sample import Sample

Config = namedtuple("Config", "effects min_qual min_samples_per_gene min_samples_per_variant min_variants_per_gene genes ignore_heterozygosity filter_db")

class Result:
    def __init__(self):
        self.samples = set()
        self.symbols = set()
        self.effect = 0
        self.maxqual = 0
        self.heterozygot = 0

def run(case,
    control,
    effects=0,
    min_qual=50,
    min_samples_per_gene=1,
    min_samples_per_variant=1,
    min_variants_per_gene=1,
    genes=[],
    control_groups=[],
    ignore_heterozygosity=True,
    db=[],
    ):

    return None

    config = Config(
        effects,
        min_qual,
        min_samples_per_gene,
        min_samples_per_variant,
        min_variants_per_gene,
        [g.encode() for g in genes],
        ignore_heterozygosity,
        len(db) > 0,
    )

    case = [Sample(c) for c in case]
    control = [Sample(c) for c in control]
    control_groups = [Group(c) for c in control_groups]

    chromosomes = list(map(str, list(range(1,23)) + ["X"]))

    case_variants = [s.variants(chromosomes=chromosomes, db=["dbsnp142"], fields=[]) for s in case]
    sample_control_keys = [s.variants(chromosomes=chromosomes, db=["dbsnp142"], fields=["key"])["key"] for s in control]
    group_control_keys = []

    # filter the variants
    # build the filter containing of all control samples and the information from the group datas
    if len(sample_control_keys) + len(group_control_keys):
        control_keys = np.unique(np.concatenate(sample_control_keys + group_control_keys))
    else:
        control_keys = np.array([], dtype=np.int64)

    d = defaultdict(lambda: Result()) # stores the samples

    for i, variants in zip(range(len(case_variants)), case_variants):
        keys = variants["key"]

        remaining = variants[np.logical_not(np.in1d(keys, control_keys))]

        for r in remaining:
            key = int(r["key"])
            item = d[key]
            item.key = key
            item.chrom = r["chrom"]
            item.typ = r["typ"]
            item.position = r["position"]
            item.chrom = "1"
            item.typ = 1
            item.position = 123
            item.samples.add(i)
            item.symbols.add(r["gene_id"])
            item.effect |= r["effect"]
            item.maxqual = int(max(item.maxqual, r["qual"]))
            item.heterozygot |= 1 if (key & 1) == 1 else 2
            item.ref = chr(r["ref"])


def main(args):
    out(run(args.case, args.control))


def out(x):
    pass
#    for i in x:
#        print(i.key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-case", nargs="+")
    parser.add_argument("-control", nargs="+")
    args = parser.parse_args()

    main(args)
