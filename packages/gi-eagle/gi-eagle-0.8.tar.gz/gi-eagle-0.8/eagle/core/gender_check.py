import argparse
from collections import namedtuple
import h5py
from eagle.core.wrap.sample import Sample


GenderEstimation = namedtuple("GenderEstimation", "name reads_y reads_x ratio est_gender")

def run(samples, divider=0.02):
    for sample in samples:
        s = Sample(sample)
        reads_y = s.readcount("Y")
        reads_x = s.readcount("X")
        ratio = reads_y / reads_x
        est_gender = "m" if ratio > divider else "f"

        yield GenderEstimation(s.samplename, reads_y, reads_x, ratio, est_gender)


def out(estimations):
    for e in estimations:
        print(e.name, e.reads_y, e.reads_x, e.ratio, e.est_gender, sep="\t")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("samples", nargs="+")
    parser.add_argument("divider", type=float, default=0.02)

    #TODO quality filter
    args = parser.parse_args()

    out(run(args.samples, args.divider))


if __name__ == "__main__":
    main()
