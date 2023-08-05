from eagle.tests.common import get_random_sample, get_random_group, setup_module

def test_call_counts():
    from eagle.core.call_counts import run
    args = (get_random_sample(True),0)
    print("run('%s',%d)" % args)
    run(*args)

def test_gender_check():
    from eagle.core.gender_check import run
    args = ([get_random_sample(True)],)
    print("run(%s)" % args)
    run(*args)

def test_purity_estimation():
    from eagle.core.gender_check import run
    args = (get_random_sample(True), get_random_sample(True))
    print("run('%s', '%s')" % args)
    run(*args)

def test_recessive():
    from eagle.core.recessive import run
    index = get_random_sample(True)
    parent1 = get_random_sample(True)
    parent2 = get_random_sample(True)
    filters = [] #[get_random_sample(True) for i in range(3)]
    args = (index, parent1, parent2, filters)
    print("run('%s', '%s', '%s', %s)" % args)
    run(*args)

def test_snps():
    from eagle.core.snps import run
    case = [get_random_sample(True) for i in range(2)]
    control = [get_random_sample(True) for i in range(2)]
    groups = [get_random_group(True)]
    args = (case, control, groups)
    print("run('%s', '%s', control_groups=%s)" % args)
    run(case, control, control_groups=groups)

def test_test():
    from eagle.core.test import run
    case = [get_random_sample(True) for i in range(2)]
    control = [get_random_sample(True) for i in range(2)]
    groups = [get_random_group(True)]
    args = (case, control, groups)
    print("run('%s', '%s', control_groups=%s)" % args)
    run(case, control, control_groups=groups)

def test_variant_detail():
    from eagle.core.variant_detail import run
    from eagle.core.wrap.sample import Sample
    import random
    sample = get_random_sample(True)
    sample_object = Sample(sample)
    chrom = random.choice(list(sample_object.f["variants"]))
    args = (sample, chrom, -1, None)
    print("run('%s', '%s', %s, %s)" % args)
    run(*args)

def test_variant_overlap():
    from eagle.core.variant_overlap import run
    s1 = get_random_sample(True)
    s2 = get_random_sample(True)
    s3 = get_random_sample(True)
    args = (s1, s2, s3)
    print("run('%s', '%s', '%s')" % args)
    run(*args)

def test_variant_search():
    from eagle.core.variant_search import run, parse_region
    from eagle.core.wrap.sample import Sample
    import random

    sample = get_random_sample(True)
    chroms = [c for c in list(Sample(sample).f["variants"].keys()) if len(c) < 3]
    regions = [parse_region("%s:%i" % (random.choice(chroms),random.randint(100000,1000000))) \
               for i in range(3)]
    args = (sample, regions)
    print("run(%s, %s)" % args)
    run(*args)
