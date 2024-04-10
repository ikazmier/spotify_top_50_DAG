from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.data_collector import collect_then_upload_json_raw_data_to_gcs
from scripts.data_transformer import (
    collect_then_transform_then_upload_json_processed_data_to_gcs,
)
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)
from airflow.providers.google.cloud.transfers.gcs_to_gcs import (
    GCSToGCSOperator,
)

from airflow.models import Variable

BQ_PROJECT_ID = Variable.get("BQ_PROJECT_ID")
BQ_DATASET = Variable.get("BQ_DATASET")
BQ_TABLE = Variable.get("BQ_TABLE")
GCS_BUCKET_NAME = Variable.get("GCS_BUCKET_NAME")


# Generate the timestamp string
def add_current_date_time_to_destination_blob_name(destination_blob_name):
    current_date_time = datetime.now().strftime("%d.%m.%Y")
    destination_blob_name_with_timestamp = (
        f"{destination_blob_name}_{current_date_time}.json"
    )
    return destination_blob_name_with_timestamp


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "spotify_data_collection",
    default_args=default_args,
    description="A DAG that collects Spotify API data in JSON format, processes it and sends it to BigQuery table.",
    schedule_interval=None,
)

collect_then_upload_json_raw_data_to_gcs_stage = PythonOperator(
    task_id="collect_then_upload_json_raw_data_to_gcs_stage",
    python_callable=collect_then_upload_json_raw_data_to_gcs,
    op_kwargs={
        "playlist_id": "37i9dQZEVXbLRQDuF5jeBp",
        "market": "US",
        "destination_bucket_name": GCS_BUCKET_NAME,
        "destination_blob_name": "JSON_RAW_API_data/stage/json_raw_playlist_data",
    },
    dag=dag,
)

collect_then_transform_then_upload_json_processed_data_to_gcs_stage = PythonOperator(
    task_id="collect_then_transform_then_upload_json_processed_data_to_gcs_stage",
    python_callable=collect_then_transform_then_upload_json_processed_data_to_gcs,
    op_kwargs={
        "source_bucket_name": GCS_BUCKET_NAME,
        "blob_prefix": "JSON_RAW_API_data/stage/json_raw_playlist_data",
        "destination_bucket_name": GCS_BUCKET_NAME,
        "destination_blob_name": "JSON_PROCESSED_API_data/stage/json_processed_playlist_data",
    },
    dag=dag,
)


move_json_raw_data_from_gcs_stage_to_archive = GCSToGCSOperator(
    task_id="move_json_raw_data_from_gcs_stage_to_archive",
    source_bucket=GCS_BUCKET_NAME,
    source_object="JSON_RAW_API_data/stage/json_raw_playlist_data",
    destination_bucket=GCS_BUCKET_NAME,
    destination_object=add_current_date_time_to_destination_blob_name(
        "JSON_RAW_API_data/archive/json_raw_playlist_data"
    ),
    move_object=True,
    dag=dag,
)


load_json_processed_data_from_gcs_stage_to_bigquery = GCSToBigQueryOperator(
    task_id="load_json_processed_data_from_gcs_to_bigquery",
    bucket=GCS_BUCKET_NAME,
    source_objects=[
        "JSON_PROCESSED_API_data/stage/json_processed_playlist_data"
    ],
    destination_project_dataset_table=f"{BQ_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}",
    schema_fields=[
        {"name": "playlist_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "playlist_name", "type": "STRING", "mode": "NULLABLE"},
        {
            "name": "playlist_number_of_followers",
            "type": "INTEGER",
            "mode": "NULLABLE",
        },
        {
            "name": "track_added_timestamp",
            "type": "TIMESTAMP",
            "mode": "NULLABLE",
        },
        {"name": "song_name", "type": "STRING", "mode": "NULLABLE"},
        {"name": "song_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "song_popularity", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "song_duration_ms", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "album_name", "type": "STRING", "mode": "NULLABLE"},
        {"name": "album_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "artist_name", "type": "STRING", "mode": "REPEATED"},
        {"name": "artist_id", "type": "STRING", "mode": "REPEATED"},
    ],
    skip_leading_rows=1,
    source_format="NEWLINE_DELIMITED_JSON",
    write_disposition="WRITE_APPEND",
    autodetect=False,
    dag=dag,
)

move_json_processed_data_from_gcs_stage_to_archive = GCSToGCSOperator(
    task_id="move_json_processed_data_from_gcs_stage_to_archive",
    source_bucket=GCS_BUCKET_NAME,
    source_object="JSON_PROCESSED_API_data/stage/json_processed_playlist_data",
    destination_bucket=GCS_BUCKET_NAME,
    destination_object=add_current_date_time_to_destination_blob_name(
        "JSON_PROCESSED_API_data/archive/json_proc  essed_playlist_data"
    ),
    move_object=True,
    dag=dag,
)

# task execution order
(
    collect_then_upload_json_raw_data_to_gcs_stage
    >> collect_then_transform_then_upload_json_processed_data_to_gcs_stage
    >> [
        move_json_raw_data_from_gcs_stage_to_archive,
        load_json_processed_data_from_gcs_stage_to_bigquery,
    ]
)

(
    load_json_processed_data_from_gcs_stage_to_bigquery
    >> move_json_processed_data_from_gcs_stage_to_archive
)
