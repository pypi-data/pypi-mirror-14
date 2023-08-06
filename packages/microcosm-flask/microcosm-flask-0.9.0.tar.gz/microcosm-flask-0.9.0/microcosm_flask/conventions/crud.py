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
from microcosm_flask.naming import collection_path_for, instance_path_for, name_for
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
def register_search_endpoint(graph, obj, path_prefix, func, request_schema, response_schema):
    """
    Register a search endpoint.

    :param graph: the object graph
    :param obj: the target resource or resource name
    :param path_prefix: the routing path prefix
    :param func: a search function, which must:
      - accept kwargs for the query string (minimally for pagination)
      - return a tuple of (items, count) where count is the total number of items
        available (in the case of pagination)
    :param request_schema: a marshmallow schema to decode/validate query string arguments
    :param response_schema: a marshmallow schema to encode (a single) response item
    """

    paginated_list_schema = make_paginated_list_schema(obj, response_schema)()

    @graph.route(path_prefix + collection_path_for(obj), Operation.Search, obj)
    @qs(request_schema)
    @response(paginated_list_schema)
    def search(**path_data):
        request_data = load_query_string_data(request_schema)
        page = Page.from_query_string(request_data)
        items, count = func(**merge_data(path_data, request_data))
        # TODO: use the schema for encoding
        return jsonify(
            PaginatedList(obj, page, items, count, response_schema).to_dict()
        )

    search.__doc__ = "Search the collection of all {}".format(pluralize(name_for(obj)))


@_crud(Operation.Create)
def register_create_endpoint(graph, obj, path_prefix, func, request_schema, response_schema):
    """
    Register a create endpoint.

    :param graph: the object graph
    :param obj: the target resource or resource name
    :param path_prefix: the routing path prefix
    :param func: a create function, which must:
      - accept kwargs for the request and path data
      - return a new item
    :param request_schema: a marshmallow schema to decode/validate request data
    :param response_schema: a marshmallow schema to encode response data

    """
    @graph.route(path_prefix + collection_path_for(obj), Operation.Create, obj)
    @request(request_schema)
    @response(response_schema)
    def create(**path_data):
        request_data = load_request_data(request_schema)
        response_data = func(**merge_data(path_data, request_data))
        return dump_response_data(response_schema, response_data, Operation.Create.value.default_code)

    create.__doc__ = "Create a new {}".format(name_for(obj))


@_crud(Operation.Retrieve)
def register_retrieve_endpoint(graph, obj, path_prefix, func, response_schema):
    """
    Register a retrieve endpoint.

    :param graph: the object graph
    :param obj: the target resource or resource name
    :param path_prefix: the routing path prefix
    :param func: a retrieve function, which must:
      - accept kwargs for path data
      - return an item or falsey
    :param response_schema: a marshmallow schema to encode response data

    """
    @graph.route(path_prefix + instance_path_for(obj), Operation.Retrieve, obj)
    @response(response_schema)
    def retrieve(**path_data):
        response_data = require_response_data(func(**path_data))
        return dump_response_data(response_schema, response_data)

    retrieve.__doc__ = "Retrieve a {} by id".format(name_for(obj))


@_crud(Operation.Delete)
def register_delete_endpoint(graph, obj, path_prefix, func):
    """
    Register a delete endpoint.

    :param graph: the object graph
    :param obj: the target resource or resource name
    :param path_prefix: the routing path prefix
    :param func: a delete function, which must:
      - accept kwargs for path data
      - return truthy/falsey

    """
    @graph.route(path_prefix + instance_path_for(obj), Operation.Delete, obj)
    def delete(**path_data):
        require_response_data(func(**path_data))
        return "", Operation.Delete.value.default_code

    delete.__doc__ = "Delete a {} by id".format(name_for(obj))


@_crud(Operation.Replace)
def register_replace_endpoint(graph, obj, path_prefix, func, request_schema, response_schema):
    """
    Register a replace endpoint.

    :param graph: the object graph
    :param obj: the target resource or resource name
    :param path_prefix: the routing path prefix
    :param func: a replace function, which must:
      - accept kwargs for the request and path data
      - return the replaced item
    :param request_schema: a marshmallow schema to decode/validate request data
    :param response_schema: a marshmallow schema to encode response data

    """
    @graph.route(path_prefix + instance_path_for(obj), Operation.Replace, obj)
    @request(request_schema)
    @response(response_schema)
    def replace(**path_data):
        request_data = load_request_data(request_schema)
        # Replace/put should create a resource if not already present, but we do not
        # enforce these semantics at the HTTP layer. If `func` returns falsey, we
        # will raise a 404.
        response_data = require_response_data(func(**merge_data(path_data, request_data)))
        return dump_response_data(response_schema, response_data)

    replace.__doc__ = "Create or update a {} by id".format(name_for(obj))


@_crud(Operation.Update)
def register_update_endpoint(graph, obj, path_prefix, func, request_schema, response_schema):
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
    @graph.route(path_prefix + instance_path_for(obj), Operation.Update, obj)
    @request(request_schema)
    @response(response_schema)
    def update(**path_data):
        # NB: using partial here means that marshmallow will not validate required fields
        request_data = load_request_data(request_schema, partial=True)
        response_data = require_response_data(func(**merge_data(path_data, request_data)))
        return dump_response_data(response_schema, response_data)

    update.__doc__ = "Update some or all of a {} by id".format(name_for(obj))


def configure_crud(graph, obj, mappings, path_prefix=""):
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
    for operation, register in CRUD_MAPPINGS.items():
        if operation in mappings:
            register(graph, obj, path_prefix, *mappings[operation])
