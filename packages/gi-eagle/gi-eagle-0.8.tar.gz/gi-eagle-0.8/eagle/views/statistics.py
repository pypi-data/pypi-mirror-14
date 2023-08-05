from flask import render_template

from eagle.application import app
from eagle.core.wrap.sample import Sample
from eagle.views.common import sample_filename, available_samples

@app.route("/statistics")
def statistics():
    samples = [Sample(sample_filename(s)) for s in available_samples()]
    return render_template("statistics.html", samples=samples)

