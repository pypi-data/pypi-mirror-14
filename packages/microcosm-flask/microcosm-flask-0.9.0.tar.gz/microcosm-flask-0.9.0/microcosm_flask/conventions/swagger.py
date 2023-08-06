"""
Swagger (OpenAPI) convention.

Exposes swagger definitions for matching operations.

"""
from flask import jsonify, g

from microcosm.api import defaults
from microcosm_flask.conventions.registry import iter_operations
from microcosm_flask.naming import singleton_path_for
from microcosm_flask.operations import Operation
from microcosm_flask.swagger.definitions import build_swagger


def register_swagger_endpoint(graph, name, version, path_prefix, match_func):
    """
    Register a swagger endpoint for a set of operations.

    """
    @graph.route(path_prefix + singleton_path_for(name), Operation.Discover, name)
    def discover():
        operations = list(iter_operations(graph, match_func))

        swagger = build_swagger(graph, version, path_prefix, operations)

        g.hide_body = True

        return jsonify(swagger)

    return name


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

    matches = {
        Operation.from_name(operation_name.lower())
        for operation_name in graph.config.swagger_convention.operations
    }

    def match_func(operation, obj, rule):
        return (
            rule.rule.startswith(base_path + path_prefix) and
            operation in matches
        )

    return register_swagger_endpoint(graph, name, version, path_prefix, match_func)
