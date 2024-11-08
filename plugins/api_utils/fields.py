"""Module for api and dataset fields data class."""

from dataclasses import dataclass


@dataclass
class Field:
    """"Data class storing information about the field in the data process

Args:
    api_field_name: a name of a field in the api documentation.
    db_field_name: a name of a field (column) in the destination dataset.
    db_data_type: a data type of a field (column) in the destination dataset.
    """

    api_field_name: str
    db_field_name: str
    db_data_type: str



