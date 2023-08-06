"""
Conventions for canonical CRUD endpoints.

"""
from flask import jsonify
from inflection import pluralize

from microcosm_flask.conventions.encoding import (
    dump_response_data,
    load_query_string_data,
    load_request_data,
    merge_data,
    require_response_data,
)
from microcosm_flask.conventions.registry import qs, request, response
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.paging import Page, PaginatedList, make_paginated_list_schema


# local registry of CRUD mappings
CRUD_MAPPINGS = {}


def _crud(operation):
    """
    Register a "register_<foo>_endpoint" function with an operation.

    """
    def decorator(func):
        CRUD_MAPPINGS[operation] = func
        return func
    return decorator


@_crud(Operation.Search)
def register_search_endpoint(graph, ns, func, request_schema, response_schema):
    """
    Register a search endpoint.

    :param graph: the object graph
    :param ns: the namespace
    :param func: a search function, which must:
      - accept kwargs for the query string (minimally for pagination)
      - return a tuple of (items, count) where count is the total number of items
        available (in the case of pagination)
    :param request_schema: a marshmallow schema to decode/validate query string arguments
    :param response_schema: a marshmallow schema to encode (a single) response item
    """

    paginated_list_schema = make_paginated_list_schema(ns, response_schema)()

    @graph.route(ns.collection_path, Operation.Search, ns)
    @qs(request_schema)
    @response(paginated_list_schema)
    def search(**path_data):
        request_data = load_query_string_data(request_schema)
        page = Page.from_query_string(request_data)
        items, count = func(**merge_data(path_data, request_data))
        # TODO: use the schema for encoding
        return jsonify(
            PaginatedList(ns, page, items, count, response_schema).to_dict()
        )

    search.__doc__ = "Search the collection of all {}".format(pluralize(ns.subject_name))


@_crud(Operation.Create)
def register_create_endpoint(graph, ns, func, request_schema, response_schema):
    """
    Register a create endpoint.

    :param graph: the object graph
    :param ns: the namespace
    :param func: a create function, which must:
      - accept kwargs for the request and path data
      - return a new item
    :param request_schema: a marshmallow schema to decode/validate request data
    :param response_schema: a marshmallow schema to encode response data

    """
    @graph.route(ns.collection_path, Operation.Create, ns)
    @request(request_schema)
    @response(response_schema)
    def create(**path_data):
        request_data = load_request_data(request_schema)
        response_data = func(**merge_data(path_data, request_data))
        return dump_response_data(response_schema, response_data, Operation.Create.value.default_code)

    create.__doc__ = "Create a new {}".format(ns.subject_name)


@_crud(Operation.Retrieve)
def register_retrieve_endpoint(graph, ns, func, response_schema):
    """
    Register a retrieve endpoint.

    :param graph: the object graph
    :param ns: the namespace
    :param func: a retrieve function, which must:
      - accept kwargs for path data
      - return an item or falsey
    :param response_schema: a marshmallow schema to encode response data

    """
    @graph.route(ns.instance_path, Operation.Retrieve, ns)
    @response(response_schema)
    def retrieve(**path_data):
        response_data = require_response_data(func(**path_data))
        return dump_response_data(response_schema, response_data)

    retrieve.__doc__ = "Retrieve a {} by id".format(ns.subject_name)


@_crud(Operation.Delete)
def register_delete_endpoint(graph, ns, func):
    """
    Register a delete endpoint.

    :param graph: the object graph
    :param ns: the namespace
    :param func: a delete function, which must:
      - accept kwargs for path data
      - return truthy/falsey

    """
    @graph.route(ns.instance_path, Operation.Delete, ns)
    def delete(**path_data):
        require_response_data(func(**path_data))
        return "", Operation.Delete.value.default_code

    delete.__doc__ = "Delete a {} by id".format(ns.subject_name)


@_crud(Operation.Replace)
def register_replace_endpoint(graph, ns, func, request_schema, response_schema):
    """
    Register a replace endpoint.

    :param graph: the object graph
    :param ns: the namespace
    :param func: a replace function, which must:
      - accept kwargs for the request and path data
      - return the replaced item
    :param request_schema: a marshmallow schema to decode/validate request data
    :param response_schema: a marshmallow schema to encode response data

    """
    @graph.route(ns.instance_path, Operation.Replace, ns)
    @request(request_schema)
    @response(response_schema)
    def replace(**path_data):
        request_data = load_request_data(request_schema)
        # Replace/put should create a resource if not already present, but we do not
        # enforce these semantics at the HTTP layer. If `func` returns falsey, we
        # will raise a 404.
        response_data = require_response_data(func(**merge_data(path_data, request_data)))
        return dump_response_data(response_schema, response_data)

    replace.__doc__ = "Create or update a {} by id".format(ns.subject_name)


@_crud(Operation.Update)
def register_update_endpoint(graph, ns, func, request_schema, response_schema):
    """
    Register an update endpoint.

    :param graph: the object graph
    :param obj: the target resource or resource name
    :param path_prefix: the routing path prefix
    :param func: an update function, which must:
      - accept kwargs for the request and path data
      - return an updated item
    :param request_schema: a marshmallow schema to decode/validate request data
    :param response_schema: a marshmallow schema to encode response data

    """
    @graph.route(ns.instance_path, Operation.Update, ns)
    @request(request_schema)
    @response(response_schema)
    def update(**path_data):
        # NB: using partial here means that marshmallow will not validate required fields
        request_data = load_request_data(request_schema, partial=True)
        response_data = require_response_data(func(**merge_data(path_data, request_data)))
        return dump_response_data(response_schema, response_data)

    update.__doc__ = "Update some or all of a {} by id".format(ns.subject_name)


def configure_crud(graph, ns, mappings, path_prefix=""):
    """
    Register CRUD endpoints for a resource object.

    :param mappings: a dictionary from operations to tuple, where each tuple contains
                     the target function and zero or more marshmallow schemas according
                     to the signature of the "register_<foo>_endpoint" functions

    Example mapping:

        {
            Operation.Create: (create_foo, NewFooSchema(), FooSchema()),
            Operation.Delete: (delete_foo,),
            Operation.Retrieve: (retrieve_foo, FooSchema()),
        }

    """
    ns = Namespace.make(ns, path=path_prefix)
    for operation, register in CRUD_MAPPINGS.items():
        if operation in mappings:
            register(graph, ns, *mappings[operation])
