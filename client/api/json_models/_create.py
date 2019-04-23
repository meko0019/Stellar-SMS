import typing

import sqlalchemy

from client.api import APIException
from client.api.json_models import BaseJSONModeler


class JSONModelCreator(BaseJSONModeler):
    """Factory that can take JSON and output a model with all
    required fields."""

    def create(self, json):
        model_kwargs = {}
        required_values = []
        type_errors = []

        for col in self.model.__table__.columns:
            assert isinstance(col, sqlalchemy.Column)

            col_name = col.name.rstrip("_")
            if col.primary_key and isinstance(
                col.type, (sqlalchemy.Integer, sqlalchemy.SmallInteger)
            ):
                if col_name in json:
                    raise APIException(
                        f"The field `{col_name}` should not be given. "
                        f"Will be decided by the database."
                    )
                continue

            # If a value can be nullable or has a default.
            value = json.get(col_name, None)
            if value is None:
                if col.nullable or (
                    col.default is not None or col.server_default is not None
                ):
                    continue
                else:
                    required_values.append(col_name)
                    continue

            value, type_error = self.convert_value_json_to_model(
                col.type, value, col.nullable
            )
            if type_error is not None:
                type_errors.append((col_name, type_error))

            model_kwargs[col.name] = value

        if len(required_values):
            raise APIException(
                f"The following required fields were not "
                f'found: `{"`, `".join(required_values)}`'
            )
        if len(type_errors):
            errors = "`, `".join(
                f"{name} should be {type_}" for name, type_ in type_errors
            )
            raise APIException(f"The following fields had the wrong type: `{errors}`")

        return self.model(**model_kwargs)
