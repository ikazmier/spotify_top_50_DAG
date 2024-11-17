"""Module for SpotifyToGCSOperator."""

import logging
from typing import Sequence

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.utils.context import Context
from api_utils.spotify.playlist.report_configuration import ReportConfiguration
from hooks.spotify_api import SpotifyApiHook
from requests import request


# pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-positional-arguments
class SpotifyToGCSOperator(BaseOperator):
    """Operator for obtaining Spotify API data and sending it to Google Cloud Storage (GCS)."""

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
        """Initialize of SpotifyToGCSOperator instance.

        Args:
            api_connection_id: a name of the connection to Spotify API.
            report_config: a configuration of the raport that is to be obtained via Spotify API.
            gcs_connection_id: a name of the connection to GCS.
            gcs_bucket_name: a name of the bucket in GCS where obtained data is to be sent.
            gcs_object_name: a name of the data object (blob) for obtained data in GCS.
            gcp_project_id: an ID of the GCP project where obtained data is to be sent to GCP.
            gcs_storage_class: a class of the bucket in GCS to be created if it doesn't exist.
            gcs_location: a location for bucket in GCS that will be creater if it doesn't exist.
            *args: an additional parameters to be passed into the class intance.
            **kwargs: an additional parameters to be passed into the class intance.
        """
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
        """Obtain data from Spotify API.

        Args:
            api_hook: an instance of SpotifyApiHook that is used to obtain data.
        Returns:
            Data obtained via API in form of Bytes.
        """
        token = api_hook.get_spotify_api_token()

        request_header = {"Authorization": f"Bearer  {token}"}
        request_url = self.report_config.report_request_url
        response = request(
            method="GET", url=request_url, headers=request_header, timeout=60
        )
        if response.status_code == 200:

            logging.info(
                "API data was obtained successfully with status code: %s",
                response.status_code,
            )
        else:
            raise AirflowException(
                f"Response not returned. Status code:{response.status_code}"
            )
        return response.content

    def _gcs_bucket_exists_check(self, gcs_hook: GCSHook) -> bool:
        """Check if bucket already exists in the GCS.

        Args:
            gcs_hook: an instance of GCS Hook.
        Returns:
            Bolean that indicates if bucket already exists in the GCS.
        """
        gcs_client = gcs_hook.get_conn()
        gcs_client_response = gcs_client.list_buckets()
        buckets = [bucket.name for bucket in gcs_client_response]
        print(buckets)
        if self.gcs_bucket_name in buckets:
            return True

        return False

    def _gcs_object_exists_check(self, gcs_hook: GCSHook) -> bool:
        """Check if object already exists in the GCS.

        Args:
            gcs_hook: an instance of GCS Hook.
        Returns:
            Bolean that indicates if object already exists in the GCS.
        """
        if gcs_hook.exists(
            bucket_name=self.gcs_bucket_name, object_name=self.gcs_object_name
        ):
            raise AirflowException(
                (
                    f"Object with name {self.gcs_object_name} already exists in the"
                    f" {self.gcs_bucket_name} bucket on the Google Cloud Storage."
                )
            )
        return False

    def _send_data_to_gcs(self, gcs_hook: GCSHook, api_data: bytes) -> None:
        """Send obained data to GCS bucket.

        Args:
            gcs_hook: an instance of GCS hook.
            api_data: a data obtained via API that is ment to be sent to GCS bucket.
        Returns:
            None.
        """
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
                (
                    "Object with name %s was successfully uploaded"
                    " to the %s bucket on the Google Cloud Storage."
                ),
                self.gcs_object_name,
                self.gcs_bucket_name,
            )

    def execute(self, context: Context) -> None:
        """Execute the process of collecting Spotify API data and sending it to GCP bucket.

        Args:
            context: an Airflow context.
        Returns:
            None.
        """
        api_hook = SpotifyApiHook(api_connection_id="spotify_api")
        api_data = self._get_api_data(api_hook=api_hook)

        gcs_hook = GCSHook(gcp_conn_id=self.gcs_connection_id)
        self._send_data_to_gcs(gcs_hook=gcs_hook, api_data=api_data)
