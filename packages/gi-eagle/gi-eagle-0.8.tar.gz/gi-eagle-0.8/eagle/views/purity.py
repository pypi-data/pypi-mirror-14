from flask import render_template, request
from collections import namedtuple

from eagle.application import app
from eagle.views.common import available_sample_objects, sample_filename, available_groups
from eagle.core import purity_estimation as purity_estimation_core


@app.route("/purity_estimation", methods=['GET', 'POST'])
def purity_estimation():
    if request.method != "POST":
        return render_template("purity_estimation_query.html", available_samples=available_sample_objects(), available_groups=available_groups())

    case_names    = request.form.getlist('case')
    control_names = request.form.getlist('control')

    Result = namedtuple("Result", "sample purity std")

    results = []
    for case, control in zip(case_names, control_names):
        purity, std = purity_estimation_core.run(sample_filename(case), sample_filename(control))
        results.append(Result(case, purity, std))

    return render_template("purity_estimation_results.html", results=results)
