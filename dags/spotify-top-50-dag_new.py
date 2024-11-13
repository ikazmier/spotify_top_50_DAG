from datetime import datetime
from airflow import DAG
from operators.spotify_api import SpotifyToGCSOperator

from reports.spotify.playlist_report import PLAYLIST_REPORT


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}

with DAG(
    "spotify_top-50-playlist-data_collection",
    default_args=default_args,
    description="A DAG that collects Spotify API data in JSON format, processes it and sends it to BigQuery table.",
    schedule_interval=None,
):

    spotify_to_gcs = SpotifyToGCSOperator(task_id = "spotify_to_gcs", api_connection_id="spotify_api", report_config= PLAYLIST_REPORT)



spotify_to_gcs