import datetime
import typing

from sqlalchemy.orm import Query
from sqlalchemy.sql import or_

from client.api import APIException
from client.api.json_models import BaseJSONModeler


class JSONModelQueryBuilder(BaseJSONModeler):
    """This object gets handed a database model and then
    is intelligent enough to build a query for both comparisons
    and range queries given a querystring.
    """

    def query(self, query: Query, args: typing.Dict[str, str]) -> Query:
        columns = {
            col_name.rstrip("_"): col
            for col_name, col in self.model.__table__.columns.items()
        }
        invalid_query = []
        type_errors = []

        queryfields = getattr(self.model, "__table_queryfields__", {})

        for key in args:
            # page and per_page are handled within paginated_response()
            if key in ["page", "per_page"]:
                continue

            value = args[key]

            operator = "="
            if key[-1] in [">", "<", "!"]:
                operator = key[-1]
                key = key[:-1]

            # Attempt to convert the string argument into
            # a type compatible with SQLAlchemy queries.
            # We check columns and hybrid_properties registered
            # within __table_queryfields__.
            if key in queryfields:
                col = getattr(self.model, key)
                col_type, is_nullable = queryfields[key]
                value, type_error = self.convert_value_json_to_model(
                    col_type, value, is_nullable
                )
            elif key in columns:
                col = columns[key]
                value, type_error = self.convert_value_json_to_model(
                    col.type, value, col.nullable
                )
            else:
                invalid_query.append(key)
                continue

            if type_error is not None:
                type_errors.append((key, type_error))
                continue

            # Don't allow `>` or `<` to be used for `null` values.
            if value is None and operator in [">", "<"]:
                raise APIException(
                    f"Values of `null` cannot be used with the `{operator}` operator"
                )

            if (
                value is None
                or not key.endswith("_at")
                or isinstance(value, datetime.datetime)
            ):
                if operator == "=":
                    query = query.filter(col == value)
                elif operator == ">":
                    query = query.filter(col >= value)
                elif operator == "<":
                    query = query.filter(col <= value)
                elif operator == "!":
                    query = query.filter(col != value)
                continue

            # If we get a date for == then that means we need to be inclusive
            # on the whole day because we store all *_at values as datetimes.
            elif isinstance(value, datetime.date):
                if operator == "=":
                    query = query.filter(
                        col
                        >= datetime.datetime.combine(
                            value, datetime.datetime.min.time()
                        ),
                        col
                        <= datetime.datetime.combine(
                            value, datetime.datetime.max.time()
                        ),
                    )
                elif operator == ">":
                    query = query.filter(
                        col
                        >= datetime.datetime.combine(
                            value, datetime.datetime.min.time()
                        )
                    )
                elif operator == "<":
                    query = query.filter(
                        col
                        <= datetime.datetime.combine(
                            value, datetime.datetime.max.time()
                        )
                    )
                elif operator == "!":
                    query = query.filter(
                        or_(
                            col
                            < datetime.datetime.combine(
                                value, datetime.datetime.min.time()
                            ),
                            col
                            > datetime.datetime.combine(
                                value, datetime.datetime.max.time()
                            ),
                        )
                    )
                continue

            invalid_query.append(key)

        if len(invalid_query) > 0:
            raise APIException(f'Could not find fields `{"`, `".join(invalid_query)}`')
        if len(type_errors):
            errors = "`, `".join(
                f"{name} should be {type_}" for name, type_ in type_errors
            )
            raise APIException(f"The following fields had the wrong type: `{errors}`")

        return query
