from flask import render_template

from eagle.application import app
from eagle.core import gender_check as gender_check_core
from eagle.views.common import available_samples, sample_filename

@app.route("/gender_check")
def gender_check():
    estimations=gender_check_core.run(map(sample_filename, available_samples()))
    return render_template("gender_check.html", estimations=estimations)
