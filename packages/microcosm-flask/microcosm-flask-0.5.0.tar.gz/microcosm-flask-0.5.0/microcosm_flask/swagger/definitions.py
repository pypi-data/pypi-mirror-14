"""
Generates a Swagger definition for registered operations.


Note that:
 -  Swagger operations and type names use different conventions from the internal definitions
    because we want to make usage friendly for code generation (e.g. bravado)

 -  Marshmallow to JSON Schema conversion is somewhat simplistic. There are several projects
    that already implement this conversion that we could try adapting. At the moment, the
    overhead of adapting another library's conventions is too high.

 -  All resource definitions are assumed to be shared and are declared in the "definitions"
    section of the result.

 -  All errors are defined generically.


"""
from werkzeug.routing import BuildError

from openapi import model as swagger

from microcosm_flask.conventions.registry import (
    get_qs_schema,
    get_request_schema,
    get_response_schema,
)
from microcosm_flask.errors import ErrorSchema, ErrorContextSchema, SubErrorSchema
from microcosm_flask.naming import name_for
from microcosm_flask.swagger.naming import operation_name, type_name
from microcosm_flask.swagger.schema import build_parameter, build_schema


def build_swagger(graph, version, path_prefix, operations):
    """
    Build out the top-level swagger definition.

    """
    base_path = graph.config.route.path_prefix
    schema = swagger.Swagger(
        swagger="2.0",
        info=swagger.Info(
            title=graph.metadata.name,
            version=version,
        ),
        consumes=swagger.MediaTypeList([
            swagger.MimeType("application/json"),
        ]),
        produces=swagger.MediaTypeList([
            swagger.MimeType("application/json"),
        ]),
        basePath=base_path + "/" + version,
        paths=swagger.Paths(),
        definitions=swagger.Definitions(),
    )
    add_paths(schema.paths, base_path + path_prefix, operations)
    add_definitions(schema.definitions, operations)
    schema.validate()
    return schema


def add_paths(paths, path_prefix, operations):
    """
    Add paths to swagger.

    """
    for operation, obj, rule, func in operations:
        path = build_path(operation, obj)[len(path_prefix):]
        method = operation.value.method.lower()
        paths.setdefault(path, swagger.PathItem())[method] = build_operation(operation, obj, rule, func)


def add_definitions(definitions, operations):
    """
    Add definitions to swagger.

    """
    # general error schema per errors.py
    for error_schema_class in [ErrorSchema, ErrorContextSchema, SubErrorSchema]:
        error_schema = error_schema_class()
        definitions[type_name(name_for(error_schema))] = swagger.Schema(build_schema(error_schema))

    # add all request and response schemas
    for operation, obj, rule, func in operations:
        request_schema = get_request_schema(func)
        if request_schema:
            definitions.setdefault(type_name(name_for(request_schema)), swagger.Schema(build_schema(request_schema)))

        response_schema = get_response_schema(func)
        if response_schema:
            definitions.setdefault(type_name(name_for(response_schema)), swagger.Schema(build_schema(response_schema)))


def build_path(operation, obj):
    """
    Build a path URI for an operation.

    """
    try:
        return operation.url_for(obj)
    except BuildError as error:
        uri_templates = {
            argument: "{{{}}}".format(argument)
            for argument in error.suggested.arguments
        }
        return operation.url_for(obj, **uri_templates)


def body_param(schema):
    return swagger.BodyParameter(**{
        "name": "body",
        "in": "body",
        "schema": swagger.JsonReference({
            "$ref": "#/definitions/{}".format(type_name(name_for(schema))),
        }),
    })


def query_param(name, field, required=False):
    """
    Build a query parameter definition.

    """
    parameter = build_parameter(field)
    parameter["name"] = name
    parameter["in"] = "query"
    parameter["required"] = False

    return swagger.QueryParameterSubSchema(**parameter)


def path_param(name, param_type="string"):
    """
    Build a path parameter definition.

    """
    return swagger.PathParameterSubSchema(**{
        "name": name,
        "in": "path",
        "required": True,
        "type": param_type,
    })


def build_operation(operation, obj, rule, func):
    """
    Build an operation definition.

    """
    swagger_operation = swagger.Operation(
        operationId=operation_name(operation, obj),
        parameters=swagger.ParametersList([
        ]),
        responses=swagger.Responses(),
        tags=[name_for(obj[0] if isinstance(obj, (list, tuple)) else obj)],
    )

    # path parameters
    swagger_operation.parameters.extend([
        # TODO: inject type information for parameters based on converter syntax
        path_param(argument)
        for argument in rule.arguments
    ])

    # query string parameters
    qs_schema = get_qs_schema(func)
    if qs_schema:
        swagger_operation.parameters.extend([
            query_param(name, field)
            for name, field in qs_schema.fields.items()
        ])

    # body parameter
    request_schema = get_request_schema(func)
    if request_schema:
        swagger_operation.parameters.append(
            body_param(request_schema)
        )

    add_responses(swagger_operation, operation, obj, func)
    return swagger_operation


def add_responses(swagger_operation, operation, obj, func):
    """
    Add responses to an operation.

    """
    # default error
    swagger_operation.responses["default"] = build_response(
        description="An error occcurred",
        resource=type_name(name_for(ErrorSchema())),
    )
    # resources response
    swagger_operation.responses[str(operation.value.default_code)] = build_response(
        description=getattr(func, "__doc__") or "{} {}".format(operation.value.name, name_for(obj)),
        resource=get_response_schema(func),
    )


def build_response(description, resource=None):
    """
    Build a response definition.

    """
    response = swagger.Response(
        description=description,
    )
    if resource is not None:
        response.schema = swagger.JsonReference({
            "$ref": "#/definitions/{}".format(type_name(name_for(resource))),
        })
    return response
