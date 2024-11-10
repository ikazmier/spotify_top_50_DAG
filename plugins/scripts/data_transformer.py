# import pandas as pd
# from google.cloud import storage
# import json


# def collect_then_transform_then_upload_json_processed_data_to_gcs(
#     source_bucket_name,
#     blob_prefix,
#     destination_bucket_name,
#     destination_blob_name,
# ):
#     json_playlist_data = download_json_from_gcs(source_bucket_name, blob_prefix)
#     df_final = transform_json_into_df(json_playlist_data)

#     df_final["artist_name"] = df_final["artist_name"].apply(json.loads)
#     df_final["artist_id"] = df_final["artist_id"].apply(json.loads)

#     send_playlist_json_to_gcs(
#         destination_bucket_name, destination_blob_name, df_final
#     )


# def download_json_from_gcs(source_bucket_name, blob_prefix):
#     storage_client = storage.Client()
#     blobs = list(
#         storage_client.list_blobs(
#             bucket_or_name=source_bucket_name, prefix=blob_prefix
#         )
#     )

#     if len(blobs) == 1:
#         blob = blobs[0]
#         json_data = blob.download_as_string()
#         return json.loads(json_data)
#     elif len(blobs) > 1:
#         print(
#             f"More than one blob found with prefix '{blob_prefix}' in bucket '{source_bucket_name}'."
#         )
#     else:
#         print(
#             f"No blob found with prefix '{blob_prefix}' in bucket '{source_bucket_name}'."
#         )

#     return None


# def transform_json_into_df(json_playlist_data, json_path=["tracks", "items"]):
#     df_from_normalized_json = pd.json_normalize(json_playlist_data, json_path)

#     # create artist_name and artis_id from unnested artists column
#     df_from_normalized_json["artist_name"] = df_from_normalized_json.apply(
#         lambda row: extract_parameter_list_from_nested_column(
#             row, "track.artists", "name"
#         ),
#         axis=1,
#     )
#     df_from_normalized_json["artist_id"] = df_from_normalized_json.apply(
#         lambda row: extract_parameter_list_from_nested_column(
#             row, "track.artists", "id"
#         ),
#         axis=1,
#     )

#     # add playlist metadata from json
#     df_from_normalized_json["playlist_id"] = json_playlist_data["id"]
#     df_from_normalized_json["playlist_name"] = json_playlist_data["name"]
#     df_from_normalized_json["number_of_followers"] = json_playlist_data[
#         "followers"
#     ]["total"]

#     # create final dataframe
#     df_final = df_from_normalized_json[
#         [
#             "playlist_id",
#             "playlist_name",
#             "number_of_followers",
#             "added_at",
#             "track.name",
#             "track.id",
#             "track.popularity",
#             "track.duration_ms",
#             "track.album.name",
#             "track.album.id",
#             "artist_name",
#             "artist_id",
#         ]
#     ]

#     # rename columns
#     df_final.columns = [
#         "playlist_id",
#         "playlist_name",
#         "playlist_number_of_followers",
#         "track_added_timestamp",
#         "song_name",
#         "song_id",
#         "song_popularity",
#         "song_duration_ms",
#         "album_name",
#         "album_id",
#         "artist_name",
#         "artist_id",
#     ]

#     return df_final


# def extract_parameter_list_from_nested_column(
#     row, nested_column_name, parameter_name
# ):
#     parameter_list = []
#     nested_column = row[nested_column_name]
#     for item in nested_column:
#         if parameter_name in item:
#             parameter_list.append(item[parameter_name])

#     return json.dumps(parameter_list)


# def send_playlist_json_to_gcs(
#     destination_bucket_name, destination_blob_name, df_final
# ):
#     json_data = df_final.to_json(orient="records", lines=True)

#     client = storage.Client()
#     bucket = client.bucket(destination_bucket_name)
#     blob = bucket.blob(destination_blob_name)
#     try:
#         blob.upload_from_string(json_data, content_type="application/json")
#         print(
#             f"Uploaded {destination_blob_name} to Google Cloud Storage as JSON."
#         )
#     except Exception as e:
#         print(f"Failed to upload {destination_blob_name} as JSON: {e}")
