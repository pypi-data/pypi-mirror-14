'''calculate the samples signature'''
import matplotlib
matplotlib.use('Agg')

import sys
import matplotlib.pyplot as plt
import numpy as np
import argparse
from collections import namedtuple, Counter
from eagle.core.wrap.sample import Sample
from itertools import product
import seaborn as sns
import pandas as pd
sns.set_style("whitegrid")


def out(x):
    pass


def fields_view(arr, fields):
    dtype2 = np.dtype({name:arr.dtype.fields[name] for name in fields})
    return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)


def stats(c):
    ret = []
    for ref in "CT":
        for alt in "ACGT".replace(ref, ""):
            for cl in "ACGT":
                for cr in "ACGT":
                    key = ((cl + ref + cr).encode(), "ACGT".index(alt))
                    yield key, c[key]
    return ret


def run(sample_filenames):
    samples = [Sample(filename) for filename in sample_filenames]
    c = Counter()

    for s in samples:
        print(s, file=sys.stderr)
        for chrom in s.chromosomes:
            variants = s.variants(chrom=chrom, fields=["key", "context"],min_qual=200, decodekey=True)
            contexts = variants["context"]
            typs = variants["typ"]
            c += Counter(zip(contexts, typs))

    keys, counts = zip(*stats(c))

    a = pd.DataFrame({'counts':counts, 'index':keys})

    sns.barplot(x="index", y="counts", data=a)
    plt.savefig("test.pdf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("samples", nargs="+")
    args = parser.parse_args()

    run(args.samples)
#    out(run(args.sample, regions))


if __name__ == "__main__":
    main()
