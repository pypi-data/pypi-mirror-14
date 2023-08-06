"""
A naming convention and discovery mechanism for HTTP endpoints.

Operations provide a naming convention for references between endpoints,
allowing easy construction of links or audit trails for external consumption.

"""
from collections import namedtuple
from urllib import urlencode
from urlparse import urljoin

from enum import Enum, unique
from flask import request, url_for

from microcosm_flask.naming import name_for


# metadata for an operation
OperationInfo = namedtuple("OperationInfo", ["name", "method", "pattern", "default_code"])


NODE_PATTERN = "{}.{}"
EDGE_PATTERN = "{}.{}.{}"


@unique
class Operation(Enum):
    """
    An enumerated set of operation types, which know how to resolve themselves into
    URLs and hrefs.

    """
    # discovery operation
    Discover = OperationInfo("discover", "GET", NODE_PATTERN, 200)

    # collection operations
    Search = OperationInfo("search", "GET", NODE_PATTERN, 200)
    Create = OperationInfo("create", "POST", NODE_PATTERN, 201)
    # bulk update is possible here with PATCH

    # instance operations
    Retrieve = OperationInfo("retrieve", "GET", NODE_PATTERN, 200)
    Delete = OperationInfo("delete", "DELETE", NODE_PATTERN, 204)
    Replace = OperationInfo("replace", "PUT", NODE_PATTERN, 200)
    Update = OperationInfo("update", "PATCH", NODE_PATTERN, 200)

    # relation operations
    CreateFor = OperationInfo("create_for", "POST", EDGE_PATTERN, 201)
    SearchFor = OperationInfo("search_for", "GET", EDGE_PATTERN, 200)

    # ad hoc operations
    Command = OperationInfo("command", "POST", NODE_PATTERN, 200)
    Query = OperationInfo("query", "GET", NODE_PATTERN, 200)

    def name_for(self, obj):
        """
        Generate an operation name in the scope of one or more resources.

        This naming convention matches how Flask blueprints routes are resolved
        (assuming that the blueprint and resources share the same name).

        Examples: `foo.search`, `bar.search_for.baz`

        """
        if isinstance(obj, (list, tuple)):
            return self.value.pattern.format(
                name_for(obj[0]),
                self.value.name,
                name_for(obj[1])
            )
        else:
            return self.value.pattern.format(
                name_for(obj),
                self.value.name,
            )

    def url_for(self, obj, **kwargs):
        """
        Construct a URL for an operation against a resource.

        :param kwargs: additional arguments for URL path expansion

        """
        return url_for(self.name_for(obj), **kwargs)

    def href_for(self, obj, qs=None, **kwargs):
        """
        Construct an full href for an operation against a resource.

        :parm qs: the query string dictionary, if any
        :param kwargs: additional arguments for path expansion
        """
        return "{}{}".format(
            urljoin(request.url_root, self.url_for(obj, **kwargs)),
            "?{}".format(urlencode(qs)) if qs else "",
        )

    @classmethod
    def from_name(cls, name):
        for operation in cls:
            if operation.value.name == name:
                return operation
        else:
            raise ValueError(name)

    @classmethod
    def parse(cls, name):
        """
        Convert an operation name back to an operation, obj tuple.

        """
        parts = name.split(".")
        operation = cls.from_name(parts[1])
        if len(parts) > 2:
            return operation, parts[0:1] + parts[2:]
        else:
            return operation, parts[0]
