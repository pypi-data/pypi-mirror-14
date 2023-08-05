import os, re
from flask import request, send_file, Response
from eagle.application import app
from eagle.views.common import bam_filename

@app.route('/bam/<accession>')
def bam(accession):
    base = accession.rstrip(".bai").rstrip(".bam")
    filename = bam_filename(base)
    if accession.endswith(".bai"):
        filename += ".bai"
    return send_file_partial(filename)


def send_file_partial(path, mimetype="application/octet-stream"):
    """
    Simple wrapper around send_file which handles HTTP 206 Partial Content
    (byte ranges)
    Taken from http://blog.asgaard.co.uk/t/flask
    TODO: handle all send_file args, mirror send_file's error handling
    (if it has any)
    """

    range_header = request.headers.get('Range', None)

    if not range_header:
        return send_file(path, mimetype=mimetype)

    size = os.path.getsize(path)
    byte1, byte2 = 0, None

    m = re.search('(\d+)-(\d*)', range_header)
    g = m.groups()

    if g[0]: byte1 = int(g[0])
    if g[1]: byte2 = int(g[1]) + 1

    byte2 = min(size, byte2)

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1

    data = None
    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data,
        206,
        mimetype=mimetype,
        direct_passthrough=True)

    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size))

    return rv
