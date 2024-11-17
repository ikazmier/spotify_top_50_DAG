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
        gcs_connection_id: str,
        gcs_bucket_name: str,
        gcs_object_name: str,
        gcp_project_id: str,
        gcs_storage_class: str,
        gcs_location: str,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.api_connection_id = api_connection_id
        self.report_config = report_config
        self.gcs_connection_id = gcs_connection_id
        self.gcs_bucket_name = gcs_bucket_name
        self.gcs_object_name = gcs_object_name
        self.gcp_project_id = gcp_project_id
        self.gcs_storage_class = gcs_storage_class
        self.gcs_location = gcs_location

    template_fields: Sequence[str] = (
        "api_connection_id",
        "gcs_connection_id",
        "gcs_bucket_name",
        "gcs_object_name",
        "gcp_project_id",
    )

    def _get_api_data(self, api_hook: SpotifyApiHook) -> bytes:

        token = api_hook.get_spotify_api_token()

        request_header = {"Authorization": f"Bearer  {token}"}
        request_url = self.report_config.report_request_url
        response = request(method="GET", url=request_url, headers=request_header)
        if response.status_code == 200:

            logging.info("API data was retrieved successfully with status code: %s", response.status_code) 
        else:
            raise AirflowException(
                f"Response not returned. Status code:{response.status_code}"
            )
        return response.content

    def _gcs_bucket_exists_check(self, gcs_hook: GCSHook) -> bool:
        gcs_client = gcs_hook.get_conn()
        gcs_client_response = gcs_client.list_buckets()
        buckets = [bucket.name for bucket in gcs_client_response]
        print(buckets)
        if self.gcs_bucket_name in buckets:
            return True

        return False

    def _gcs_object_exists_check(self, gcs_hook: GCSHook) -> bool:
        if gcs_hook.exists(
            bucket_name=self.gcs_bucket_name, object_name=self.gcs_object_name
        ):
            raise AirflowException(
                f"Object with name {self.gcs_object_name} already exists in the {self.gcs_bucket_name} bucket on the Google Cloud Storage."
            )
        return False

    def _send_data_to_gcs(self, gcs_hook: GCSHook, api_data: bytes) -> None:

        if not self._gcs_bucket_exists_check(gcs_hook=gcs_hook):

            gcs_hook.create_bucket(
                bucket_name=self.gcs_bucket_name,
                storage_class=self.gcs_storage_class,
                location=self.gcs_location,
                project_id=self.gcp_project_id,
            )

        if not self._gcs_object_exists_check(gcs_hook=gcs_hook):

            gcs_hook.upload(
                bucket_name=self.gcs_bucket_name,
                object_name=self.gcs_object_name,
                data=api_data,
            )
            logging.info(
                "Object with name %s was successfully uploaded to the %s bucket on the Google Cloud Storage.", self.gcs_object_name, self.gcs_bucket_name
            )

    def execute(self, context: Context):

        api_hook = SpotifyApiHook(connection_id="spotify_api")
        api_data = self._get_api_data(api_hook=api_hook)

        gcs_hook = GCSHook(gcp_conn_id=self.gcs_connection_id)
        self._send_data_to_gcs(gcs_hook=gcs_hook,api_data=api_data)
