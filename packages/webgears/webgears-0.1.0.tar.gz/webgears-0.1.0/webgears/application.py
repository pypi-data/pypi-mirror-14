"""Application module."""

import os

import jinja2
import logging
import yaml

from werkzeug import serving
from werkzeug import exceptions

from webgears import routing
from webgears import views


class Application(object):
    """Base application."""

    rule_maps = []

    def __init__(self):
        """Initializer."""
        self.name = self.__class__.__name__

        self._config = self._init_config()
        self._app_config = self._config['app']

        self._logger = self._init_logging()

        self._router = self._init_router()
        self._jinja_env = self._init_templates_system(
            self._config['app']['templates_dir'])

        self._views = self._init_views(self._jinja_env)

    def run_simple(self):
        """Run application in development mode.

        Do not use it in production!
        """
        serving.run_simple(self._app_config.get('host', '127.0.0.1'),
                           self._app_config.get('port', 5000),
                           self,
                           use_debugger=True,
                           use_reloader=True,
                           static_files=self._app_config.get('static',
                                                             {'/static':
                                                              'static/'}))

    def __call__(self, environ, start_response):
        """Dispatch WSGI request."""
        request = views.Request(environ)

        router_adapter = self._router.bind_to_environ(request.environ)
        try:
            endpoint, values = router_adapter.match()
        except exceptions.HTTPException as exception:
            return exception(environ, start_response)
        else:
            view = self._views[endpoint]

        try:
            with view.request_context(request, router_adapter, values):
                response = view.handle_request()
        except exceptions.HTTPException as exception:
            return exception(environ, start_response)
        except Exception as exception:
            self._logger.exception(exception)
            return exceptions.ServiceUnavailable(environ, start_response)
        else:
            return response(environ, start_response)

    def _init_config(self):
        """Initialize application configuration.

        Application will check `{project_root}/etc/{application_name}.yml`
        file. Also if `{project_root}/etc/{application_name}.local.yml` exists,
        it will override main configuration options.
        """
        application_module = __import__(self.__class__.__module__)

        project_root = os.path.abspath(os.path.sep.join(
            [os.path.dirname(application_module.__file__)] + ['..'] * 2
        ))
        conf_root = os.path.sep.join((project_root, 'etc'))

        main_conf_path = os.path.sep.join((conf_root, '{0}.yml'.format(
            self.__class__.__name__.lower())))
        local_conf_path = os.path.sep.join((conf_root, '{0}.local.yml'.format(
            self.__class__.__name__.lower())))

        with open(main_conf_path) as main_conf_file:
            conf = yaml.load(main_conf_file)

        try:
            with open(local_conf_path) as local_conf_file:
                local_conf = yaml.load(local_conf_file)
        except IOError:
            pass
        else:
            conf.update(local_conf)

        return conf

    def _init_router(self):
        """Initialize application router."""
        router = routing.Router()
        for rules_map in self.__class__.rule_maps:
            router.bind_rules_map(rules_map)
        return router

    def _init_templates_system(self, templates_dir):
        """Initialize application templates system."""
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir))

    def _init_views(self, jinja_env):
        """Initialize application views."""
        return dict((rule.endpoint, rule.view_provider(jinja_env=jinja_env))
                    for rule in self._router.iter_rules())

    def _init_logging(self):
        """Initialize application loggign."""
        logging.basicConfig()
        return logging.getLogger('webgears')


__all__ = (
    'Application',
)
