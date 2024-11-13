"""Module for api and dataset fields classes."""

from dataclasses import dataclass
import enum
from typing import Any, Dict, Optional


class BigQueryDataType(enum.Enum):
    """Enumeration class for BigQuery data types."""

    BOOL = "BOOL"
    BYTES = "BYTES"
    DATE = "DATE"
    INT = "INT64"
    FLOAT = "FLOAT64"
    STR = "STRING"
    TIMESTAMP = "TIMESTAMP"
    JSON = "JSON"
    STRUCT = "STRUCT"

@dataclass
class Field:
    """Data class storing information about the field in the data process.

    Args:
        api_field_name: a name of a field in the api documentation.
        db_field_name: a name of a field (column) in the destination dataset.
        db_data_type: a data type of a field (column) in the destination dataset.
        schema: a schema of the Field if field is of JSON or STRUCT data type, defaults to None
    """

    api_field_name: str
    db_field_name: str
    db_data_type: BigQueryDataType
    schema: Optional[Dict[str, Any]] = None