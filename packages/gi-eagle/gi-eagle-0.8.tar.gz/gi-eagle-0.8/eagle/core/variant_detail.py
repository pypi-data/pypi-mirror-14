import numpy as np
from eagle.core.wrap.sample import Sample


from eagle.core.wrap.sample import Sample

def run(filename, chrom, position, typ):
    '''return all variants at the position'''
    s = Sample(filename)
    variants = s.variants(chrom, start=position, stop=position+1, fields=[])
    return variants
