"""Views module."""

import six

from werkzeug import wrappers
from werkzeug import utils
from werkzeug import exceptions

from dependency_injector import catalogs
from dependency_injector import providers

from webgears import routing
from webgears import json


class Request(wrappers.Request):
    """View request."""


class Response(wrappers.Response):
    """View response."""


class View(object):
    """Base view."""

    def __init__(self, jinja_env):
        """Initializer."""
        self._jinja_env = jinja_env

        self.handlers = dict()

        # Request handling context
        self.request = None
        self.router_adapter = None
        self.values = None

        super(View, self).__init__()

    def request_context(self, request, router_adapter, values):
        """Set request's context."""
        self.request = request
        self.router_adapter = router_adapter
        self.values = values
        return self

    def __enter__(self):
        """Enter request's context."""

    def __exit__(self, *_):
        """Reset request's context."""
        self.request = None
        self.router_adapter = None
        self.values = None

    def handle_request(self):
        """Handle request."""
        method = self.request.method
        try:
            handler = self.handlers[method]
        except KeyError:
            try:
                handler = getattr(self, method.lower())
            except AttributeError:
                return exceptions.MethodNotAllowed()
            else:
                self.handlers[method] = handler
        return handler(**self.values)

    def render_template(self, template, context=None):
        """Render template with specified context."""
        if not context:
            context = dict()
        context.update({
            'request': self.request,
            'url_for': self.url_for,
        })
        template_object = self._jinja_env.get_template(template)
        return template_object.render(context).encode('utf-8')

    def url_for(self, endpoint, values=None, method=None, force_external=False,
                append_unknown=True):
        """Build an url for specified endpoint."""
        return self.router_adapter.build(endpoint, values, method,
                                         force_external, append_unknown)

    def redirect(self, *args, **kwargs):
        """Create and return redirect response."""
        return utils.redirect(*args, **kwargs)

    def html(self, template, context=None):
        """Render template with context and return result as html response."""
        return Response(self.render_template(template, context),
                        mimetype='text/html')

    def json(self, context=None):
        """Dump context to the json and return result as json response."""
        return Response(json.dumps(context), mimetype='application/json')

    def response(self, *args, **kwargs):
        """Return general view response."""
        return Response(*args, **kwargs)


class TemplateView(View):
    """Common view for rendering templates."""

    def __init__(self, template, context=None, **kwargs):
        """Initializer."""
        self.template = template
        self.context = context
        super(TemplateView, self).__init__(**kwargs)

    def get(self):
        """Handle GET request."""
        return self.html(self.template, self.context)


class Provider(providers.Factory):
    """View provider."""

    provided_type = View


class CatalogMetaClass(catalogs.DeclarativeCatalogMetaClass):
    """View providers catalog metaclass."""

    def __new__(mcs, class_name, bases, attributes):
        """Declarative catalog meta class."""
        cls = catalogs.DeclarativeCatalogMetaClass.__new__(mcs,
                                                           class_name,
                                                           bases,
                                                           attributes)
        cls.RulesMap = type('RulesMap',
                            tuple([routing.RulesMap]),
                            {'views_catalog': cls})
        return cls


@six.add_metaclass(CatalogMetaClass)
class Catalog(catalogs.DeclarativeCatalog):
    """View providers catalog."""

    provider_type = Provider


__all__ = (
    'Request',
    'Response',
    'View',
    'Provider',
    'Catalog',
)
