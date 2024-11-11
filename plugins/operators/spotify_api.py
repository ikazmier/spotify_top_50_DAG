from enum import Enum
from typing import Sequence

from airflow.models import BaseOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.utils.context import Context
from hooks.spotify_api import SpotifyApiHook
import logging

class SpotifyToGCSOperator(BaseOperator):

    def __init__(
        self,
        api_connection_id: str,
        # gcs_connection_id: str,
        # gcs_bucket_name: str,
        # gcs_object_name: str,
        #report_config: ReportConfiguration
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.api_connection_id = api_connection_id
        # self.gcs_connection_id = gcs_connection_id
        # self.gcs_bucket_name = gcs_bucket_name
        # self.gcs_object_name = gcs_object_name

    template_fields: Sequence[str] = (
        "api_connection_id",
        # "gcs_connection_id",
        # "gcs_bucket_name",
        # "gcs_boject_name",
    )

    def execute(self, context: Context):
        
        hook = SpotifyApiHook(connection_id="spotify_api")
        token = hook.get_spotify_api_token()

        request_header = f"Authorization: Bearer  {token}"

        