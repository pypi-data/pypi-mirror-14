"""
Purity estimation as defined by Su, X. et al, 2012. Bioinformatics 28, 2265–266.
"""
import numpy as np
import h5py
import argparse
from collections import namedtuple
from eagle.core.esd import generalizedESD
from eagle.core.wrap.sample import Sample


def fields_view(arr, fields):
    dtype2 = np.dtype({name:arr.dtype.fields[name] for name in fields})
    return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)


def run(tumor_filename, normal_filename, min_qual=200):
    chrom_count = 22

    tumor = Sample(tumor_filename)
    normal = Sample(normal_filename)

    chrom_purities = []
    fields = ["key", "depth", "alt_count", "depth"]

    def fraction(values):
        alt = np.sum(values["alt_count"])
        depth = np.sum(values["depth"])

        if depth == 0:
            return -1
        return alt / depth


    for chrom in map(str, range(1, chrom_count + 1)):
        values_tumor = tumor.variants(chrom, min_qual=min_qual, het=True, fields=fields)
        values_normal = normal.variants(chrom, min_qual=min_qual, het=True, fields=fields)

        positions_tumor = np.unique(values_tumor["key"]) # no need to >> because ALL snps are het
        positions_normal = np.unique(values_normal["key"])

        #subtract control variants from case variants
        somatics = values_tumor[np.logical_not(np.in1d(positions_tumor, positions_normal))]
        allele_fraction_affected = fraction(somatics)
        allele_fraction_healthy  = fraction(values_normal)

        if allele_fraction_affected == -1 or allele_fraction_healthy == -1:
            continue


        # the first fraction is 0.5 if affected sample is pure. Sequencing can introduce bias here, hence the 0.5 is normalized with the fraction for the healthy sample.
        # purity is the quotient of the two fractions
        chrom_purity = allele_fraction_affected / allele_fraction_healthy

        # the purity estimate can exceed one (reason can be: two few/too many low quality SNPs in healthy sample). We exclude such estimates.
        print(chrom_purity)

        if chrom_purity > 1:
            continue
        chrom_purities.append(chrom_purity)

    # calculate the generalized ESD as suggested in the paper
    outlier_count, indices = generalizedESD(chrom_purities, len(chrom_purities) // 4)

    # add omitted samples to the outlier count
    outlier_count += chrom_count - len(chrom_purities)

    # remove outliers
    indices = set(indices)

    non_outlier_purities = [purity for i, purity in enumerate(chrom_purities) if i not in indices]
    if non_outlier_purities:
        purity = np.mean(non_outlier_purities)
        std = np.std(non_outlier_purities)
    else:
        purity = None
        std = None

    return (purity, std)


def out(purity, std):
    print("purity", purity)
    print("std", std)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tumor")
    parser.add_argument("normal")
    parser.add_argument("--minqual", default=0, type=int)

    #TODO quality filter
    args = parser.parse_args()

    out(*run(args.tumor, args.normal, args.minqual))


if __name__ == "__main__":
    main()
