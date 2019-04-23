import datetime
import typing

import sqlalchemy
from sqlalchemy.dialects.postgresql import JSON

from client.database import DATETIME_FORMAT

__all__ = [
    "BaseJSONModeler",
    "JSONModelCreator",
    "JSONModelQueryBuilder",
]


class BaseJSONModeler(object):
    """Base type for JSON to database modelers."""

    def __init__(self, model):
        self.model = model

    @staticmethod
    def convert_value_json_to_model(
        col_type, value, is_nullable
    ):
        """Checks a column from a model against a value from JSON. If
        the value matches the column then it will be returned otherwise
        the required type will be returned.
        """

        def is_column_type(c_t, possible_types):
            """Helper function that allows using col.type
            (ie sqlalchemy.Column(sqlalchemy.Integer).type)
            or passing a type explicitly (ie sqlalchemy.Integer)
            """
            return isinstance(c_t, possible_types) or c_t in possible_types

        # Null
        if is_nullable and value == "null":
            return None, None

        # Integers
        if is_column_type(col_type, (sqlalchemy.SmallInteger, sqlalchemy.Integer)):
            try:
                value = int(value)
            except (TypeError, ValueError):
                return None, "integer"

        # Decimal
        if is_column_type(col_type, (sqlalchemy.Numeric,)):
            try:
                value = Decimal(value)
            except ValueError:
                return None, "decimal"

        # Strings
        elif is_column_type(col_type, (sqlalchemy.String, sqlalchemy.Text)):
            if not isinstance(value, str):
                return None, "string"

        # Booleans
        elif is_column_type(col_type, (sqlalchemy.Boolean,)) and not isinstance(
            value, bool
        ):
            if isinstance(value, str):
                value_lower = value.lower()
                if value_lower == "true":
                    value = True
                elif value_lower == "false":
                    value = False
                else:
                    return None, "boolean(true,false)"
            else:
                return None, "boolean(true,false)"

        # Datetime
        elif is_column_type(col_type, (sqlalchemy.DateTime,)):
            if isinstance(value, str):
                try:
                    value = datetime.datetime.strptime(value, DATETIME_FORMAT)
                except ValueError:
                    try:
                        value = datetime.datetime.strptime(
                            value + " 00:00:00", DATETIME_FORMAT
                        )
                        value = value.date()
                    except ValueError:
                        return None, "datetime"
            else:
                return None, "datetime"

        # JSON
        elif is_column_type(col_type, (JSON,)):
            if not isinstance(value, dict):
                return None, "object"

        return value, None


from ._create import JSONModelCreator  # noqa
from ._query import JSONModelQueryBuilder  # noqa
