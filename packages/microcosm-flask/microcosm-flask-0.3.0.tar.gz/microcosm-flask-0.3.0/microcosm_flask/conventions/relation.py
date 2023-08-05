"""
Conventions for canonical relation endpoints (mapping one resource to another).

For relations, operation definitions require *two* objects instead of one; for
simplicity these are passed as a pair/tuple.

"""
from flask import jsonify

from microcosm_flask.conventions.encoding import (
    load_query_string_data,
    merge_data,
)
from microcosm_flask.naming import relation_path_for
from microcosm_flask.operations import Operation
from microcosm_flask.paging import Page, PaginatedList


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


@_relation(Operation.SearchFor)
def register_search_relation_endpoint(graph, obj, path_prefix, func, request_schema, response_schema):
    """
    Register a relation endpoint.

    :param func: a search function, which must:
      - accept kwargs for the query string (minimally for pagination)
      - return a tuple of (items, count, context) where count is the total number of items
        available (in the case of pagination) and context is a dictionary providing any
        needed context variables for constructing pagination links

    :param request_schema: a marshmallow schema to decode/validate query string arguments
    :param response_schema: a marshmallow schema to encode (a single) response item
    """
    @graph.route(path_prefix + relation_path_for(*obj), Operation.SearchFor, obj)
    def search(**path_data):
        request_data = load_query_string_data(request_schema)
        page = Page.from_query_string(request_data)
        items, count, context = func(**merge_data(path_data, request_data))
        return jsonify(
            PaginatedList(obj, page, items, count, response_schema, Operation.SearchFor, **context).to_dict()
        )


def configure_relation(graph, from_obj, to_obj, mappings, path_prefix=""):
    """
    Register relation endpoint(s) between two resources.

    """
    for operation, register in RELATION_MAPPINGS.items():
        if operation in mappings:
            register(graph, (from_obj, to_obj), path_prefix, *mappings[operation])
