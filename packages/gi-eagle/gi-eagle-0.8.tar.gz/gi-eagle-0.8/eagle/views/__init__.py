"""
EAGLE views init
"""

__all__ = [
    "index",
    "snp",
    "variant",
    "recessive",
    "purity",
    "statistics",
    "files",
    "gender_check",
    "call_counts",
]


#from exomate.database import get_session
#from exomate.application import app
#import time
#from flask import g

#session = get_session()

## to print SQL statements, enable this
##session.bind.echo = True


#@app.before_request
#def start_time_measurement():
#	g.start_time = time.time()
#	g.request_time = lambda: "%.1fs" % (time.time() - g.start_time)


#@app.teardown_request
#def shutdown_session(exception=None):
#	"""close database connection when this request is finished"""
#	session.remove()
