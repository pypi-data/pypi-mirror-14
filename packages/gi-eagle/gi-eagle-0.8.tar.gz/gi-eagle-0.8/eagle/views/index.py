"""
The index page
"""

from flask import render_template
from eagle.application import app

@app.route('/')
def index():
    return render_template('index.html')

