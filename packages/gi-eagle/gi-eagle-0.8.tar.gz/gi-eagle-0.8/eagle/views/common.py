import os, glob
from eagle.application import app
from eagle.core.wrap.sample import Sample

SNP_PATH = app.config["SNP_PATH"]
GROUP_PATH = app.config["GROUP_PATH"]
BAM_PATH = app.config["BAM_PATH"]
DATABASE_PATH = app.config["DATABASE_PATH"]

def __h5files__(path):
    '''return sorted h5 files in a path'''
    files = [f.rsplit("/", 1)[-1][:-3] for f in glob.iglob(os.path.join(path, "*.h5"))]
    return sorted(files)


def available_samples(project_filter=True):
    '''return all available sample names'''
    return __h5files__(SNP_PATH)


def available_sample_objects(project_filter=True):
    '''return all available samples as Sample objects'''
    return [Sample(sample_filename(s)) for s in available_samples()]


def available_groups(project_filter=True):
    '''return all available groups'''
    return __h5files__(GROUP_PATH)


def available_databases(project_filter=True):
    '''return all available groups'''
    return __h5files__(DATABASE_PATH)


def sample_filename(sample):
    '''return the filename to a given sample'''
    return os.path.join(SNP_PATH, sample + ".h5")


def group_filename(group):
    '''return the filename to a given sample'''
    return os.path.join(GROUP_PATH, group + ".h5")


def bam_filename(sample):
    '''return the bam filename to a given sample'''
    return os.path.join(BAM_PATH, sample + ".bam")


def database_filename(database):
    '''return the bam filename to a given database'''
    return os.path.join(DATABASE_PATH, database + ".h5")


class Query():
    pass


def parse_request(request):
    q = Query()
    q.case = request.form.getlist('case')
    q.control = request.form.getlist('control')
    q.effects = sum(request.form.getlist('effects', type=int))
    q.min_qual = request.form.get('minquality', type=int)
    q.min_mapping_qual = request.form.get('minmappingquality', type=int)
    q.min_samples_per_gene = request.form.get('samplespergene', type=int)
    q.min_samples_per_variant = request.form.get('samplespervariant', type=int)
    q.min_variants_per_gene = request.form.get('variantspergene', type=int)
    q.search_all = request.form.get('searchall', type=bool)
    q.case_groups = request.form.getlist('case_group')
    q.control_groups = request.form.getlist('control_group')
    q.ignore_heterozygosity = request.form.get('ignore_heterozygosity', type=bool) == True
    q.db = request.form.getlist('db')

    # genes
    genes = request.form.getlist('genes')
    if genes and not q.search_all:
        q.genes = map(lambda x: x.strip(), request.form.getlist('genes')[0].split("\n"))
    else:
        q.genes = []

    q.index = request.form.get('sample')
    q.parent1 = request.form.get('parent1')
    q.parent2 = request.form.get('parent2')

    return q
