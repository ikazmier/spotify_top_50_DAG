"""Module for declaring configuration of Spotify playlist report."""
from api_utils.spotify.playlist.report_configuration import (ApiEndpoint, ReportConfiguration)

TOP50_PLAYLIST_ID = ("37i9dQZEVXbMDoHDwVN2tF",)
PLAYLIST_REPORT_CONFIG = ReportConfiguration(endpoint= ApiEndpoint.PLAYLISTS, resource_ids= TOP50_PLAYLIST_ID)

 