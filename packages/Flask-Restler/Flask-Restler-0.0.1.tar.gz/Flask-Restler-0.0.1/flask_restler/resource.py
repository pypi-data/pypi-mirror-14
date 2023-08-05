from flask import request, current_app, abort
from flask._compat import with_metaclass
from flask.json import dumps
from flask.views import View

from . import APIError
from .auth import current_user


PER_PAGE_ARG = 'per_page'
PAGE_ARG = 'page'


class ResourceOptions(object):

    """Prepare resource options."""

    def __init__(self, cls):
        self.meta = meta = getattr(cls, "Meta", None)

        self.cls = cls
        for base in reversed(cls.mro()):
            if not hasattr(base, "Meta"):
                continue

            for k, v in base.Meta.__dict__.items():
                if k.startswith('__'):
                    continue
                setattr(self, k, v)

        self.name = (meta and getattr(meta, 'name', None)) or \
            cls.__name__.lower().split('resource', 1)[0]

        if self.per_page:
            self.per_page = int(self.per_page)

        if self.schema_api:
            self.schema_api = dict(self.schema_api)

        self.endpoints = getattr(self, 'endpoints', {})
        self.endpoints.update({
            value.route[1]: (value, value.route) for value in cls.__dict__.values()
            if hasattr(value, 'route') and isinstance(value.route, tuple)
        })

    def __repr__(self):
        return "<Options %s>" % self.cls


class ResourceMeta(type):

    """Do some work for resources."""

    def __new__(mcs, name, bases, params):
        cls = super(ResourceMeta, mcs).__new__(mcs, name, bases, params)
        cls.methods = set([method.upper() for method in cls.methods])
        cls.meta = cls.OPTIONS_CLASS(cls)
        return cls


class Resource(with_metaclass(ResourceMeta, View)):

    """Base API Resource object."""

    OPTIONS_CLASS = ResourceOptions

    # methods: Allowed methods
    methods = 'get',

    # Schema: Resource marshmallow schema
    Schema = None

    class Meta:

        # name: Resource's name (if it is None, it will be calculated)
        name = None

        # per_page: Paginate results (set to None for disable pagination)
        per_page = 100

        # url: URL for collection, if it is None it will be calculated
        # url_detail: URL for resource detail, if it is None it will be calculated
        url = url_detail = None

        schema_api = None

    def __init__(self, api=None, **kwargs):
        self.api = api
        return super(Resource, self).__init__(**kwargs)

    def dispatch_request(self, *args, **kwargs):
        self.auth = self.authorize(*args, **kwargs)
        self.collection = self.get_many(*args, **kwargs)
        resource = self.get_one(*args, **kwargs)

        endpoint = kwargs.pop('endpoint', None)
        if endpoint and hasattr(self, endpoint):
            method = getattr(self, endpoint)
            return method(*args, **kwargs)

        if self.meta.per_page and request.method == 'GET' and resource is None:
            try:
                per_page = int(request.args.get(PER_PAGE_ARG, self.meta.per_page))
                if per_page:
                    page = int(request.args.get(PAGE_ARG, 0))
                    offset = page * per_page
                    self.collection, total = self.paginate(offset, per_page)
            except ValueError:
                raise APIError('Pagination params are invalid.')

        try:
            if resource is not None:
                kwargs['resource'] = resource
            method = getattr(self, request.method.lower())
            response = method(*args, **kwargs)
            return current_app.response_class(
                dumps(response, indent=2), mimetype='application/json')
        except AttributeError:
            return abort(405)

    def authorize(self, *args, **kwargs):
        """Default authorization method."""
        if self.api is not None:
            return self.api.authorize(*args, **kwargs)
        return current_user

    def get_many(self, *args, **kwargs):
        return []

    def get_one(self, *args, **kwargs):
        """Load resource."""
        return kwargs.get(self.meta.name)

    def get_schema(self, resource=None):
        return self.Schema and self.Schema()

    def save(self, obj):
        """Create a resource."""
        return obj

    def to_simple(self, data, many=False):
        """Serialize response to simple object (list, dict)."""
        schema = self.get_schema()
        return schema.dump(data, many=many).data if schema else data

    def paginate(self, offset, limit):
        """Paginate results."""
        return self.collection[offset: offset + limit], len(self.collection)

    def get(self, resource=None, **kwargs):
        """Get resource or collection of resources."""
        if resource is not None and resource != '':
            return self.to_simple(resource)

        return self.to_simple(self.collection, many=True)

    def post(self, **kwargs):
        """Create a resource."""
        schema = self.get_schema()
        obj, errors = schema.load(request.json or {})
        if errors:
            raise APIError('Bad request', payload={'errors': errors})
        self.save(obj)
        return self.to_simple(obj)

    def put(self, resource=None, **kwargs):
        """Update a resource."""
        if resource is None:
            raise APIError('Resource not found', status_code=404)

        schema = self.get_schema(resource=resource)
        obj, errors = schema.load(request.json or {}, partial=True)
        if errors:
            raise APIError('Bad request', payload={'errors': errors})
        self.save(obj)
        return self.to_simple(obj)

    patch = put

    def delete(self, resource=None, **kwargs):
        """Delete a resource."""
        if resource is None:
            raise APIError('Resource not found', status_code=404)
        self.collection.remove(resource)
