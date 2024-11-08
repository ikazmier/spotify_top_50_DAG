import base64
import requests
import json
from google.cloud import storage
from airflow.models import Variable
from google.oauth2 import service_account


def collect_then_upload_json_raw_data_to_gcs(
    playlist_id, market, destination_bucket_name, destination_blob_name
):
    playlist_data = fetch_playlist_data(playlist_id, market)
    send_data_to_gcs(
        playlist_data, destination_bucket_name, destination_blob_name
    )


def fetch_playlist_data(playlist_id, market="US"):
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}?market={market}",
        headers=headers,
    )
    return response.json()


def get_spotify_token():
    client_id = Variable.get("SPOTIFY_API_CLIENT_ID")
    client_secret = Variable.get("SPOTIFY_API_CLIENT_SECRET")

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=headers,
        data={"grant_type": "client_credentials"},
    )
    token = response.json().get("access_token")
    return token


def send_data_to_gcs(data, destination_bucket_name, destination_blob_name):

    credentials_path = Variable.get("GOOGLE_APPLICATION_CREDENTIALS")
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )

    client = storage.Client(credentials=credentials)
    bucket_name = destination_bucket_name
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(json.dumps(data), content_type="application/json")
    print(f"Uploaded data to {destination_blob_name} in bucket {bucket_name}")
