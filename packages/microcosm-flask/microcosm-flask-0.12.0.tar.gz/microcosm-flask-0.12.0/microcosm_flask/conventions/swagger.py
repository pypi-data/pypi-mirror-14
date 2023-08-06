"""
Swagger (OpenAPI) convention.

Exposes swagger definitions for matching operations.

"""
from flask import jsonify, g

from microcosm.api import defaults
from microcosm_flask.conventions.registry import iter_endpoints
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.swagger.definitions import build_swagger


def register_swagger_endpoint(graph, ns, match_func):
    """
    Register a swagger endpoint for a set of operations.

    """
    @graph.route(ns.singleton_path, Operation.Discover, ns)
    def discover():
        operations = list(iter_endpoints(graph, match_func))

        swagger = build_swagger(graph, ns.version, ns.path, operations)

        g.hide_body = True

        return jsonify(swagger)

    return ns.subject


@defaults(
    name="swagger",
    operations=[
        "create",
        "delete",
        "replace",
        "retrieve",
        "search",
        "search_for",
        "update",
    ],
    path_prefix="",
)
def configure_swagger(graph):
    """
    Build a singleton endpoint that provides swagger definitions for all operations.

    """
    name = graph.config.swagger_convention.name
    version = graph.config.swagger_convention.version

    base_path = graph.config.route.path_prefix
    path_prefix = graph.config.swagger_convention.path_prefix + "/" + version

    ns = Namespace(
        path=path_prefix,
        subject=name,
        version=version,
    )

    matching_operations = {
        Operation.from_name(operation_name)
        for operation_name in graph.config.swagger_convention.operations
    }

    def match_func(operation, ns, rule):
        return (
            rule.rule.startswith(base_path + path_prefix) and
            operation in matching_operations
        )

    return register_swagger_endpoint(graph, ns, match_func)
