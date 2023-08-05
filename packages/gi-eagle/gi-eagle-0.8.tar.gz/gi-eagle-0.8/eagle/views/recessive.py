import os
from flask import render_template, request
from collections import namedtuple

from eagle.application import app
from eagle.views.common import sample_filename, available_sample_objects, available_groups, parse_request
from eagle.core import recessive as recessive_core
from eagle.core.effectenum import EffectNames, exon_effects


@app.route('/recessive', methods=['GET', 'POST'])
def recessive():
    if request.method != "POST":
        return render_template("recessive_query.html",
            available_samples=available_sample_objects(),
            available_groups=available_groups(),
            EffectNames=EffectNames,
            exon_effects=exon_effects
        )

    q = parse_request(request)

    index_filename = sample_filename(q.index)
    parent1_filename = sample_filename(q.parent1)
    parent2_filename = sample_filename(q.parent2)

    results = recessive_core.run(
        index_filename,
        parent1_filename,
        parent2_filename,
        effects=q.effects,
        min_qual=q.min_qual,
        db=q.db,
    )

    return render_template("recessive_results.html", results=results, query=q)
