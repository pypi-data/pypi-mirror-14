import os
from flask import render_template, request
from collections import namedtuple

from eagle.application import app
from eagle.views.common import sample_filename, available_samples, parse_request
from eagle.core import call_counts as call_counts_core

@app.route("/call_counts", methods=['GET', 'POST'])
def call_counts():
    if request.method != "POST":
        return render_template("call_counts_query.html", available_samples=available_samples())

    q = parse_request(request)

    minqual = int(request.form.get("minquality"))
    sample_filenames = [sample_filename(s) for s in request.form.getlist("samples")]
    sample_counts = call_counts_core.data(sample_filenames,minqual)

    return render_template("call_counts_results.html", results=sample_counts)
