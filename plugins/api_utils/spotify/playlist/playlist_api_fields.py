"""Module with Spotify api fields for the playlist endpoint https://developer.spotify.com/documentation/web-api/reference/get-playlist"""

from api_utils.field import BigQueryDataType, Field

COLLABORATIVE = Field(
    api_field_name="collaborative",
    db_field_name="collaborative",
    db_data_type=BigQueryDataType.BOOL,
)

DESCRIPTION = Field(
    api_field_name="description",
    db_field_name="description",
    db_data_type=BigQueryDataType.STR,
)

EXTERNAL_URLS = Field(
    api_field_name="external_urls",
    db_field_name="external_urls",
    db_data_type=BigQueryDataType.STRUCT,
    schema={"spotify": BigQueryDataType.STR},
)

FOLLOWERS = Field(
    api_field_name="followers",
    db_field_name="followers",
    db_data_type=BigQueryDataType.STRUCT,
    schema={"href": BigQueryDataType.STR, "total": BigQueryDataType.INT},
)

HREF = Field(
    api_field_name="href", db_field_name="href", db_data_type=BigQueryDataType.STR
)

ID = Field(api_field_name="id", db_field_name="id", db_data_type=BigQueryDataType.STR)

IMAGES = Field(
    api_field_name="images",
    db_field_name="images",
    db_data_type=BigQueryDataType.STRUCT,
    schema={
        "url": BigQueryDataType.STR,
        "height": BigQueryDataType.INT,
        "width": BigQueryDataType.INT,
    },
)

NAME = Field(
    api_field_name="name", db_field_name="name", db_data_type=BigQueryDataType.STR
)

OWNER = Field(
    api_field_name="owner",
    db_field_name="owner",
    db_data_type=BigQueryDataType.STRUCT,
    schema={
        "external_urls": {"spotify": BigQueryDataType.STR},
        "followers": {"href": BigQueryDataType.STR, "total": BigQueryDataType.INT},
        "href": BigQueryDataType.STR,
        "id": BigQueryDataType.STR,
        "type": BigQueryDataType.STR,
        "uri": BigQueryDataType.STR,
        "display_name": BigQueryDataType.STR,
    },
)

PUBLIC = Field(
    api_field_name="public", db_field_name="public", db_data_type=BigQueryDataType.BOOL
    ),

SNAPSHOT_ID = Field(
    api_field_name="snapshot_id", db_field_name="snapshot_id", db_data_type=BigQueryDataType.BOOL
    ),

TRACKS = Field(
    api_field_name="tracks",
    db_field_name="tracks",
    db_data_type=BigQueryDataType.STRUCT,
    schema={
        "href": BigQueryDataType.STR,
        "limit": BigQueryDataType.INT,
        "next": BigQueryDataType.STR,
        "offset": BigQueryDataType.INT,
        "previous": BigQueryDataType.STR,
        "total": BigQueryDataType.INT,
        "items": {
            "added_at": BigQueryDataType.STR,
            "added_by": {
                "external_urls": {"spotify": BigQueryDataType.STR},
                "followers": {
                    "href": BigQueryDataType.STR,
                    "total": BigQueryDataType.INT
                },
                "href": BigQueryDataType.STR,
                "id": BigQueryDataType.STR,
                "type": BigQueryDataType.STR,
                "uri": BigQueryDataType.STR,
            },
            "is_local": BigQueryDataType.BOOL,
            "track": {
                "album": {
                    "album_type": BigQueryDataType.STR,
                    "total_tracks": BigQueryDataType.INT,
                    "available_markets": BigQueryDataType.STRUCT,  
                    "external_urls": {"spotify": BigQueryDataType.STR},
                    "href": BigQueryDataType.STR,
                    "id": BigQueryDataType.STR,
                    "images": {
                        "url": BigQueryDataType.STR,
                        "height": BigQueryDataType.INT,
                        "width": BigQueryDataType.INT,
                    },
                    "name": BigQueryDataType.STR,
                    "release_date": BigQueryDataType.STR,
                    "release_date_precision": BigQueryDataType.STR,
                    "restrictions": {"reason": BigQueryDataType.STR},
                    "type": BigQueryDataType.STR,
                    "uri": BigQueryDataType.STR,
                    "artists": [
                        {
                            "external_urls": {"spotify": BigQueryDataType.STR},
                            "href": BigQueryDataType.STR,
                            "id": BigQueryDataType.STR,
                            "name": BigQueryDataType.STR,
                            "type": BigQueryDataType.STR,
                            "uri": BigQueryDataType.STR,
                        }
                    ]
                },
                "artists": [
                    {
                        "external_urls": {"spotify": BigQueryDataType.STR},
                        "href": BigQueryDataType.STR,
                        "id": BigQueryDataType.STR,
                        "name": BigQueryDataType.STR,
                        "type": BigQueryDataType.STR,
                        "uri": BigQueryDataType.STR,
                    }
                ],
                "available_markets": BigQueryDataType.STRUCT,  
                "disc_number": BigQueryDataType.INT,
                "duration_ms": BigQueryDataType.INT,
                "explicit": BigQueryDataType.BOOL,
                "external_ids": {
                    "isrc": BigQueryDataType.STR,
                    "ean": BigQueryDataType.STR,
                    "upc": BigQueryDataType.STR,
                },
                "external_urls": {"spotify": BigQueryDataType.STR},
                "href": BigQueryDataType.STR,
                "id": BigQueryDataType.STR,
                "is_playable": BigQueryDataType.BOOL,
                "linked_from": BigQueryDataType.STRUCT,  
                "restrictions": {"reason": BigQueryDataType.STR},
                "name": BigQueryDataType.STR,
                "popularity": BigQueryDataType.INT,
                "preview_url": BigQueryDataType.STR,
                "track_number": BigQueryDataType.INT,
                "type": BigQueryDataType.STR,
                "uri": BigQueryDataType.STR,
                "is_local": BigQueryDataType.BOOL,
            }
        }
    }
)

TYPE = Field(
    api_field_name="type", db_field_name="type", db_data_type=BigQueryDataType.STR
    ),

URI = Field(
    api_field_name="uri", db_field_name="uri", db_data_type=BigQueryDataType.STR
    ),