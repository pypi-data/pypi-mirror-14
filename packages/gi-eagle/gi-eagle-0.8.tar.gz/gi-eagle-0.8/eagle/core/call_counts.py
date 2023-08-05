import argparse
from eagle.core.wrap.sample import Sample


def data(samples, minqual):
    sample_counts = dict()
    for sample in samples:
        s = Sample(sample)
        count = sum([len(s.variants(c, minqual)) for c in s.chromosomes])
        yield {"sample": s.basename, "count": count}


def out(data):
    for x in data:
        print("%s: %d" % (x["sample"], x["count"]))
#    if len(samples) > 1:
#        print("Total: %d" % sum(counts.values()))


def run(args):
    out(data(args.samples, args.minqual))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("samples", nargs='+')
    parser.add_argument("--minqual", type=int)

    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
