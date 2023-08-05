'''determine the sample's variants in a given region'''

import numpy as np
import argparse
from collections import namedtuple
from eagle.core.wrap.sample import Sample
from numpy.lib.recfunctions import append_fields, merge_arrays

Region = namedtuple("Region", "chrom start stop")

'''parse the region string and return region namedtuple'''
def parse_region(r):
    chrom, position_range = r.split(":")
    if position_range.find("-") > -1:
        start, stop = position_range.split("-")
    else:
        start = int(position_range)
        stop = position_range
        print(start, stop)
    return Region(chrom, int(start), int(stop)+1)


def run(sample, regions, database=False):
    s = Sample(sample)

    if database:
        fields=["key", "id"]
    else:
        fields=["key", "qual", "ref"]

    for region in regions:
        variants = s.variants(chrom=region.chrom, start=region.start, stop=region.stop, fields=fields, decodekey=True)
        yield variants


index_to_base = "ACGTMIDE"

def out(variants):
    for var in variants:
        for v in var:
            print(v["chrom"], v["position"], v["qual"], chr(v["ref"]), index_to_base[v["typ"]], sep="\t")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sample")
    parser.add_argument("region")
    args = parser.parse_args()

    regions = [parse_region(args.region)]
    out(run(args.sample, regions))


if __name__ == "__main__":
    main()
