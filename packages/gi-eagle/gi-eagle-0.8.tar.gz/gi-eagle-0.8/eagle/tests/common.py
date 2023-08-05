from testconfig import config
import random

def get_random_sample(path=False):
    from eagle.views.common import available_samples, sample_filename
    sample = random.choice(available_samples())
#    print("Random Sample: %s" % sample)
    if path:
        return sample_filename(sample)
    return sample

def get_random_group(path=False):
    from eagle.views.common import available_groups, group_filename
    group = random.choice(available_groups())
  #  print("Random Group: %s" % group)
    if path:
        return group_filename(group)
    return group


def setup_module(module):
    from eagle.application import app
    if not "conf" in config.keys():
        config['conf'] = 'config.cfg'
    app._readconfig_(config['conf'])

