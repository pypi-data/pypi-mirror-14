"""
A discovery endpoint provides links to other endpoints.

"""
from flask import jsonify

from microcosm.api import defaults
from microcosm_flask.conventions.encoding import load_query_string_data
from microcosm_flask.conventions.registry import iter_endpoints
from microcosm_flask.linking import Link, Links
from microcosm_flask.namespaces import Namespace
from microcosm_flask.paging import Page, PageSchema
from microcosm_flask.operations import Operation


def iter_links(operations, page):
    """
    Generate links for an iterable of operations on a starting page.

    """
    for operation, ns, rule, func in operations:
        yield Link.for_(
            operation=operation,
            ns=ns,
            type=ns.subject_name,
            qs=page.to_tuples(),
        )


def register_discovery_endpoint(graph, ns, match_func):
    """
    Register a discovery endpoint for a set of operations.

    """
    page_schema = PageSchema()

    @graph.route(ns.singleton_path, Operation.Discover, ns)
    def discover():
        # accept pagination limit from request
        page = Page.from_query_string(load_query_string_data(page_schema))
        page.offset = 0

        operations = list(iter_endpoints(graph, match_func))

        return jsonify(
            _links=Links({
                "self": Link.for_(Operation.Discover, ns, qs=page.to_tuples()),
                "search": [
                    link for link in iter_links(operations, page)
                ],
            }).to_dict()
        )

    return ns.subject


@defaults(
    name="",
    operations=[
        "search",
    ],
    path_prefix="",
)
def configure_discovery(graph):
    """
    Build a singleton endpoint that provides a link to all search endpoints.

    """
    ns = Namespace(
        path=graph.config.discovery_convention.path_prefix,
        subject=graph.config.discovery_convention.name,
    )

    matching_operations = {
        Operation.from_name(operation_name)
        for operation_name in graph.config.discovery_convention.operations
    }

    def match_func(operation, ns, rule):
        return operation in matching_operations

    return register_discovery_endpoint(graph, ns, match_func)
