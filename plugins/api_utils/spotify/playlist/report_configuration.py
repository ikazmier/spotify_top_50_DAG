"""Module for report configuration class."""

from enum import Enum
from typing import Tuple


class ApiEndpoint(Enum):
    """Enumeration class for Spotify API endpoints."""

    ARTISTS = "artists"
    ARTIST_ALBUMS = ["artists", "albums"]
    ARTIST_TRACKS = ["artists", "tracks"]
    ARTIST_RELATED_ARTISTS = ["artists", "related-artists"]
    AUDIOBOOKS = "audiobooks"
    AUDIOBOOKS_CHAPTERS = ["audiobooks", "chapters"]
    CHAPTERS = "chapters"
    EPISODES = "episodes"
    PLAYLISTS = "playlists"
    SHOWS = "shows"
    SHOW_EPISODES = ["shows", "episodes"]
    TRACKS = "tracks"
    AUDIOFEATURES = "audio-features"
    AUDIOANALYSIS = "audio-analysis"


class ReportConfiguration:
    """Class for configuration of Spotify API report."""
    
    def __init__(
        self,
        endpoint: ApiEndpoint,
        resource_ids: Tuple[str, ...],
        api_version: str = "v1",
        **additional_request_params,
    ):
        """Initialize ReportConfiguration instance.

        Args:
            endpoint: an instance of ApiEndpoint.
            resouce_ids: an id of an Spotify resource.
            api_version: a version of API to be used, defaults to "v1".
            **additional_request_params: an additional reqest params to be passed into request url.
        """
        self.endpoint = endpoint
        self.resource_ids = resource_ids
        self.api_version = api_version
        self.additional_request_params = additional_request_params

    @property
    def additional_request_params_str(self) -> str:
        """An additional request params to be passed into API request."""
        if self.additional_request_params:
            params_list = [
                f"{key}={value}"
                for key, value in self.additional_request_params.items()
            ]
            params_request_str = f"&{'&'.join(params_list)}"
            return params_request_str
        return ""

    @property
    def report_request_url(self) -> str:
        """A report url to be passed into API reqest.

        Returns:
            A request URL.
        """
        if len(self.resource_ids) == 1:
            if isinstance(self.endpoint.value, list):
                request_url = (
                    f"https://api.spotify.com/{self.api_version}/"
                    f"{self.endpoint.value[0]}/{self.resource_ids[0]}/"
                    f"{self.endpoint.value[1]}{self.additional_request_params_str}"
                )
            else:
                request_url = (
                    f"https://api.spotify.com/{self.api_version}/"
                    f"{self.endpoint.value}/{self.resource_ids[0]}"
                    f"{self.additional_request_params_str}"
                )
        else:
            request_url = (
                f"https://api.spotify.com/{self.api_version}/"
                f"{self.endpoint.value}?ids={'%2C'.join(self.resource_ids)}"
                f"{self.additional_request_params_str}"
            )
        return request_url
