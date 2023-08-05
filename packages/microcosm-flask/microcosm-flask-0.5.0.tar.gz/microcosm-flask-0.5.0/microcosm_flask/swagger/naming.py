"""
Naming conventions for Swagger definitions.

Intended to play nice with generated code (e.g. with Bravado)

"""

from inflection import camelize, pluralize

from microcosm_flask.naming import name_for


def operation_name(operation, obj):
    """
    Convert an operation, obj(s) pair into a swagger operation id.

    For compatability with Bravado, we want to use underscores instead of dots and
    verb-friendly names. Example:

        foo.retrieve       => client.foo.retrieve()
        foo.search_for.bar => client.foo.search_for_bars()

    """
    if isinstance(obj, (list, tuple)):
        verb, rest = operation.value.name, obj[1:]
    else:
        verb, rest = operation.value.name, []
    return "_".join([verb] + [pluralize(name_for(noun)) for noun in rest])


def type_name(name):
    """
    Convert an internal name into a swagger type name.

    For example:

        foo_bar => FooBar

    """
    if name.endswith("_schema"):
        name = name[:-7]
    return camelize(name)
