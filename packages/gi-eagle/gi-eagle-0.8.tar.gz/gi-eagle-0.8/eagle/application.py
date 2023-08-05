from flask import Flask
from eagle import configuration


class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


class Eagle(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config['SECRET_KEY'] = "123"

        self.wsgi_app = ReverseProxied(self.wsgi_app)

        #admin = Admin(app, name="DEEP")

        self.jinja_env.trim_blocks = True

    def _readconfig_(self, config_file):
        #configuration parsing
        conf = configuration.parse(config_file)
        self.config['SNP_PATH'] = conf.get("pathes", "snp")
        self.config['GROUP_PATH'] = conf.get("pathes", "group")
        self.config['BAM_PATH'] = conf.get("pathes", "bam")
        self.config['DATABASE_PATH'] = conf.get("pathes", "database")
        self.config['REFERENCE'] = conf.get("reference", "version", fallback="hg19")

    def run(self, *args, config="", **kwargs):
        """
        Imports all views and then runs the Flask application.
        """
        self._readconfig_(config)
        import eagle.views
        import eagle.filters as filters
        for view in eagle.views.__all__:
            __import__("eagle.views.%s" % view)
        super().run(*args, **kwargs)

app = Eagle(__name__)

if __name__ == '__main__':
    app.readconfig("config.cfg")
    app.run(debug=True)
