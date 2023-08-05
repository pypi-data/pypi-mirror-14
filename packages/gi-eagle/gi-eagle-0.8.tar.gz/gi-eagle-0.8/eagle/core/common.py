from eagle.core.wrap.sample import Sample

class NamedDict(dict):
    def __init__(self, *args, **kwargs):
        super(NamedDict, self).__init__(*args, **kwargs)


def create_sample(sample_filename):
    '''create a sample object from a given sample_filename'''
    return Sample(sample_filename)
