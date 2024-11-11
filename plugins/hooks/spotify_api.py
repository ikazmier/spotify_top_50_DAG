"""Module for Spotify API Hook."""

import logging
from base64 import b64encode
from typing import Dict

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from requests import request


class SpotifyApiHook(BaseHook):
    """Airflow Hook to interact with the Spotify API."""

    def __init__(self, connection_id: str, *args, **kwargs):
        """Initialize the SpotifyApiHook instance.

        Args:
            connection_id: a string name of the connection to Spotify API.
            *args: an additional parameters to be passed into the class intance.
            **kwargs: an additional parameters to be passed into the class instance.
        """
        super().__init__(*args, **kwargs)
        self.connection_id = connection_id
        self.client_required_fields = ["client_id", "client_secret"]

    def get_conn(self):
        """Return None as no traditional connection is needed for Spotify API."""
        return None

    @property
    def fetch_spotify_conn_config(self) -> Dict:
        """Fetch and validate Spotify API connection configuration.

        Returns:
            A dictionary with fetched spotify secrets needed to obtain token."""
        self.log.info("Fetching Spotify API connection: %s", self.connection_id)
        conn = self.get_connection(self.connection_id)
        config = conn.extra_dejson
        missing_keys = set(self.client_required_fields) - set(config.keys())
        if missing_keys:
            raise AirflowException(
                f"Missing required fields: {', '.join(missing_keys)}"
            )
        return config

    def get_spotify_api_token(self) -> str:
        """Get an access token from the Spotify API.

        Returns:
            A token needed to request data from Spotify API in form of string."""
        conn_config = self.fetch_spotify_conn_config
        credentials = f"{conn_config['client_id']}:{conn_config['client_secret']}"
        encoded_credentials = b64encode(credentials.encode("utf-8")).decode("utf-8")

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "client_credentials"}

        response = request(
            method="POST",
            url="https://accounts.spotify.com/api/token",
            headers=headers,
            data=data,
            timeout=60,
        )

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            logging.info("Access Token obtained successfully.")
            return access_token

        raise AirflowException(
            f"Failed to retrieve token: {response.status_code}, {response.text}"
        )
