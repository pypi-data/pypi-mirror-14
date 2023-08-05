"""
SNP query page
"""
from functools import reduce
from collections import namedtuple
from flask import render_template, request
from eagle.application import app
from eagle.views.common import sample_filename, group_filename, available_groups, available_sample_objects, parse_request, available_databases
from eagle.core import snps
from eagle.core.effectenum import EffectNames, exon_effects
from eagle.core.wrap.group import Group


@app.template_filter()
def diseases(samples):
    '''return the disease of a sample'''
    return set([sample.disease for sample in samples])


def samples_by_diseases(diseases):
    '''return all samples affected by one of the given diseases'''
    return [sample_filename(s.basename) for s in available_sample_objects() if s.disease in diseases]


@app.route('/snp', methods=['GET', 'POST'])
def snp():
    if request.method != "POST":
        return render_template("snp_query.html",
            available_samples=available_sample_objects(),
            available_groups=available_groups(),
            available_databases=available_databases(),
            EffectNames=EffectNames,
            exon_effects=exon_effects,
        )

    # parse the request parameters
    q = parse_request(request)

    #building case filenames
    cases = [sample_filename(c) for c in q.case]
    cases.extend(samples_by_diseases(q.case_groups))
    cases = set(cases)

    # building control filenames
    controls = [sample_filename(c) for c in q.control]
    controls.extend(samples_by_diseases(q.control_groups))
    controls = set(controls)

    results = snps.run(
        cases,
        controls,
        q.effects,
        q.min_qual,
        q.min_samples_per_gene,
        q.min_samples_per_variant,
        q.min_variants_per_gene,
        q.genes,
        ignore_heterozygosity=q.ignore_heterozygosity,
        db=q.db,
        min_alt_mapping_qual=q.min_mapping_qual,
    )

    return render_template('snp_results.html', results=results, query=q)
