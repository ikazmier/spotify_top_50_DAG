from enum import Enum
from typing import Sequence

from airflow.models import BaseOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.utils.context import Context
from hooks.spotify_api import SpotifyApiHook
from airflow.exceptions import AirflowException
import logging
from requests import request

from api_utils.spotify.playlist.report_configuration import ReportConfiguration

class SpotifyToGCSOperator(BaseOperator):

    def __init__(
        self,
        api_connection_id: str,
        report_config: ReportConfiguration,
        # gcs_connection_id: str,
        # gcs_bucket_name: str,
        # gcs_object_name: str,
        #report_config: ReportConfiguration
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.api_connection_id = api_connection_id
        self.report_config = report_config
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

        request_header = {"Authorization": f"Bearer  {token}"}
        request_url =self.report_config.report_request_url
        response = request(method="GET", url = request_url, headers= request_header)
        if response.status_code == 200:

            logging.info("SUCCESS: %s",response.content)
        else:
            raise AirflowException("Incorrect response ...") # tutaj daj więcej info
             
