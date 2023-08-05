"""
A discovery endpoint provides links to other endpoints.

"""
from flask import jsonify

from microcosm.api import defaults
from microcosm_flask.conventions.encoding import load_query_string_data
from microcosm_flask.linking import Link, Links
from microcosm_flask.naming import name_for, singleton_path_for
from microcosm_flask.paging import Page, PageSchema
from microcosm_flask.operations import Operation


def iter_operations(graph, match_func):
    """
    Iterate through operations in matches.

    """
    for rule in graph.flask.url_map.iter_rules():
        try:
            operation, obj = Operation.parse(rule.endpoint)
        except ValueError:
            # operation follows a different convention (e.g. "static")
            continue
        else:
            # match_func gets access to rule to support path version filtering
            if match_func(operation, obj, rule):
                yield operation, obj


def iter_links(operations, page):
    """
    Generate links for an iterable of operations on a starting page.

    """
    for operation, obj in operations:
        yield Link.for_(
            operation=operation,
            obj=obj,
            type=name_for(obj),
            qs=page.to_tuples(),
        )


def register_discovery_endpoint(graph, name, operations, path_prefix=""):
    """
    Register a discovery endpoint for a set of operations.

    """
    page_schema = PageSchema()

    @graph.route(path_prefix + singleton_path_for(name), Operation.Discover, name)
    def discover():
        # accept pagination limit from request
        page = Page.from_query_string(load_query_string_data(page_schema))
        page.offset = 0

        return jsonify(
            _links=Links({
                "self": Link.for_(Operation.Discover, name, qs=page.to_tuples()),
                "search": [
                    link for link in iter_links(operations, page)
                ],
            }).to_dict()
        )

    return name


@defaults(
    name="all",
    operations=[
        "search",
    ],
    path_prefix="",
)
def configure_discovery(graph):
    """
    Build a singleton endpoint that provides a link to all search endpoints.

    """
    name = graph.config.discovery_convention.name
    path_prefix = graph.config.discovery_convention.path_prefix

    matches = {
        Operation.from_name(operation_name.lower())
        for operation_name in graph.config.discovery_convention.operations
    }

    def match_func(operation, obj, rule):
        return operation in matches

    return register_discovery_endpoint(graph, name, iter_operations(graph, match_func), path_prefix)
