from eagle.application import app
from eagle.core.effectenum import EffectNames

@app.template_filter()
def effects(s):
    '''generate effects string from effect bitvector'''
    ret = [EffectNames[b] for b in EffectNames if b & s > 0]
    return ", ".join(ret)


_heterozygosity_strings = {1:"het", 2:"hom", 3:"both"}

@app.template_filter()
def heterozygosity(h):
    '''return the string for a heterozygosity "enum"'''
    return _heterozygosity_strings.get(h, "error")


@app.template_filter()
def single_element(s):
    '''return an element from an iteratable'''
    return next(iter(s))
