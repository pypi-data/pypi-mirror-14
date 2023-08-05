import sys
import numpy as np
import argparse
from .wrap.sample import Sample
from collections import namedtuple


class Result:
    def __init__(self):
        self.samples = set()
        self.symbols = set()
        self.effect = 0
        self.maxqual = 0
        self.heterozygot = 0


def encode_keys(variants):
    '''decode the key and append fields'''
    keys = variants["key"]
    mask = (1 << 48) - 1
    position = np.bitwise_and(keys, mask) >> 4
    mask = (1 << 4) - 1
    typ = np.bitwise_and(keys, mask) >> 1
    mask = 1
    het = np.bitwise_and(keys, mask)
#    m = append_fields(variants, data=(chroms, positions, types, het), names=("chrom_nr", "position", "typ", "het"))
    return position, typ, het, variants


def encode_key(key):
    mask = (1 << 48) - 1
    position = np.bitwise_and(key, mask) >> 4
    mask = (1 << 4) - 1
    typ = np.bitwise_and(key, mask) >> 1
    mask = 1
    het = np.bitwise_and(key, mask)
    return position, typ, het


def run(index_filename, parent1_filename, parent2_filename, filter_filenames=[], effects=0, min_qual=0, db=[]):
    index = Sample(index_filename)
    parent1 = Sample(parent1_filename)
    parent2 = Sample(parent2_filename)
    filter_samples = [Sample(f) for f in filter_filenames]

    chromosomes = list(map(str, list(range(1,23)) + ["X"]))

    for chrom in chromosomes:
        index_variants = index.variants(chrom, min_qual=min_qual, effects=effects, filter_dbs=db, fields=["key", "qual", "gene_id", "effect", "ref"])

        parent1_het = parent1.variants(chrom, het=True, filter_dbs=db, fields=["key", "gene_id"])
        parent2_het = parent2.variants(chrom, het=True, filter_dbs=db, fields=["key", "gene_id"])

        index_in_parent1 = np.in1d(index_variants["key"], parent1_het["key"])
        index_in_parent2 = np.in1d(index_variants["key"], parent2_het["key"])

        index_is_het = (index_variants["key"] & 1) == 1

        compound_parent1_genes = index_variants[index_is_het & index_in_parent1 & np.logical_not(index_in_parent2)]["gene_id"]
        compound_parent2_genes = index_variants[index_is_het & index_in_parent2 & np.logical_not(index_in_parent1)]["gene_id"]

        compound_genes = np.intersect1d(compound_parent1_genes, compound_parent2_genes)

        choosen_compound = index_is_het & np.logical_xor(index_in_parent1, index_in_parent2) & np.logical_not(index_variants["gene_id"]==b"") & np.in1d(index_variants["gene_id"], compound_genes)


        # homozygous is much easier
        choosen_homo = np.logical_not(index_is_het) & index_in_parent1 & index_in_parent2

        choosen = choosen_compound | choosen_homo

        choosen_index = index_variants[choosen]
        choosen_in_parents = (np.array((index_in_parent1, index_in_parent2)).T)[choosen]

        for r, in_p in zip(choosen_index, choosen_in_parents):
            key = int(r["key"])
            position, typ, het = encode_key(key)
            item = Result()
            item.key = key
            item.chrom = chrom
            item.typ = typ
            item.position = position
            item.symbols.add(r["gene_id"])
            item.samples.add(0)
            item.effect |= r["effect"]
            item.maxqual = int(max(item.maxqual, r["qual"]))
            item.heterozygot |= 1 if het == 1 else 2
            item.inp1 = in_p[0]
            item.inp2 = in_p[1]
            item.ref = chr(r["ref"])
            yield item


def out(chrom, r):
    print(chrom, r)


def main(args):
    run(args.tumor, args.blood)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("index")
    parser.add_argument("parent1")
    parser.add_argument("parent2")
    parser.add_argument("--control", nargs="+", default=[])
    args = parser.parse_args()

    for r in run(args.index, args.parent1, args.parent2, args.control):
        out(r)
