"""
Conventions for canonical relation endpoints (mapping one resource to another).

For relations, endpoint definitions require that the `Namespace` contain *both*
a subject and an object.

"""
from flask import jsonify
from inflection import pluralize

from microcosm_flask.conventions.encoding import (
    dump_response_data,
    load_query_string_data,
    load_request_data,
    merge_data,
)
from microcosm_flask.conventions.registry import qs, request, response
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.paging import Page, PaginatedList, make_paginated_list_schema


# local registry of relation mappings
RELATION_MAPPINGS = {}


def _relation(operation):
    """
    Register a "register_<foo>_relation_endpoint" function with an operation.

    """
    def decorator(func):
        RELATION_MAPPINGS[operation] = func
        return func
    return decorator


@_relation(Operation.CreateFor)
def register_createfor_relation_endpoint(graph, ns, func, request_schema, response_schema):
    """
    Register a create-for relation endpoint.

    :param graph: the object graph
    :param ns: the namespace
    :param path_prefix: the routing path prefix
    :param func: a store create function, which must:
      - accept kwargs for the new instance creation parameters
      - return the created instance
    :param request_schema: a marshmallow schema to decode/validate instance creation parameters
    :param response_schema: a marshmallow schema to encode the created instance
    """
    @graph.route(ns.relation_path, Operation.CreateFor, ns)
    @request(request_schema)
    @response(response_schema)
    def create(**path_data):
        request_data = load_request_data(request_schema)
        response_data = func(**merge_data(path_data, request_data))
        return dump_response_data(response_schema, response_data, Operation.CreateFor.value.default_code)

    create.__doc__ = "Create a new {} relative to a {}".format(pluralize(ns.object_name), ns.subject_name)


@_relation(Operation.SearchFor)
def register_search_relation_endpoint(graph, ns, func, request_schema, response_schema):
    """
    Register a relation endpoint.

    :param graph: the object graph
    :param ns: the namespace
    :param func: a search function, which must:
      - accept kwargs for the query string (minimally for pagination)
      - return a tuple of (items, count, context) where count is the total number of items
        available (in the case of pagination) and context is a dictionary providing any
        needed context variables for constructing pagination links
    :param request_schema: a marshmallow schema to decode/validate query string arguments
    :param response_schema: a marshmallow schema to encode (a single) response item
    """

    paginated_list_schema = make_paginated_list_schema(ns.object_ns, response_schema)()

    @graph.route(ns.relation_path, Operation.SearchFor, ns)
    @qs(request_schema)
    @response(paginated_list_schema)
    def search(**path_data):
        request_data = load_query_string_data(request_schema)
        page = Page.from_query_string(request_data)
        items, count, context = func(**merge_data(path_data, request_data))
        # TODO: use the schema for encoding
        return jsonify(
            PaginatedList(ns, page, items, count, response_schema, Operation.SearchFor, **context).to_dict()
        )

    search.__doc__ = "Search for {} relative to a {}".format(pluralize(ns.object_name), ns.subject_name)


def configure_relation(graph, ns, mappings, path_prefix=""):
    """
    Register relation endpoint(s) between two resources.

    """
    ns = Namespace.make(ns, path=path_prefix)
    for operation, register in RELATION_MAPPINGS.items():
        if operation in mappings:
            register(graph, ns, *mappings[operation])
