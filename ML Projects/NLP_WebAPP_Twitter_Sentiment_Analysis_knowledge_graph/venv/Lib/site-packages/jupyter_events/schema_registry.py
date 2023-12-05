""""An event schema registry."""
from typing import Optional, Union

from .schema import EventSchema


class SchemaRegistryException(Exception):  # noqa[N818]
    """Exception class for Jupyter Events Schema Registry Errors."""


class SchemaRegistry:
    """A convenient API for storing and searching a group of schemas."""

    def __init__(self, schemas: Optional[dict] = None):
        """Initialize the registry."""
        self._schemas = schemas or {}

    def __contains__(self, key: str) -> bool:
        """Syntax sugar to check if a schema is found in the registry"""
        return key in self._schemas

    def __repr__(self) -> str:
        """The str repr of the registry."""
        return ",\n".join([str(s) for s in self._schemas.values()])

    def _add(self, schema_obj: EventSchema) -> None:
        if schema_obj.id in self._schemas:
            msg = (
                f"The schema, {schema_obj.id}, is already "
                "registered. Try removing it and registering it again."
            )
            raise SchemaRegistryException(msg)
        self._schemas[schema_obj.id] = schema_obj

    @property
    def schema_ids(self):
        return self._schemas.keys()

    def register(self, schema: Union[dict, str, EventSchema]) -> EventSchema:
        """Add a valid schema to the registry.

        All schemas are validated against the Jupyter Events meta-schema
        found here:
        """
        if not isinstance(schema, EventSchema):
            schema = EventSchema(schema)
        self._add(schema)
        return schema

    def get(self, id: str) -> EventSchema:
        """Fetch a given schema. If the schema is not found,
        this will raise a KeyError.
        """
        try:
            return self._schemas[id]
        except KeyError:
            msg = (
                f"The requested schema, {id}, was not found in the "
                "schema registry. Are you sure it was previously registered?"
            )
            raise KeyError(msg) from None

    def remove(self, id: str) -> None:
        """Remove a given schema. If the schema is not found,
        this will raise a KeyError.
        """
        try:
            del self._schemas[id]
        except KeyError:
            msg = (
                f"The requested schema, {id}, was not found in the "
                "schema registry. Are you sure it was previously registered?"
            )
            raise KeyError(msg) from None

    def validate_event(self, id: str, data: dict) -> None:
        """Validate an event against a schema within this
        registry.
        """
        schema = self.get(id)
        schema.validate(data)
