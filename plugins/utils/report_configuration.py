"""Module for report configuration class."""
from enum import Enum
from typing import List

class ApiEndpoint(Enum):
    ALBUMS = "albums"

class ReportConfiguration:

    def __init__(self, endpoint: ApiEndpoint, resource_ids: List[str], **additional_request_params):
        self.endpoint = endpoint
        self.resource_ids = resource_ids
        self.additional_request_params = additional_request_params  # stored as a dict            

    @property
    def additional_request_params_str(self) -> str:
        if self.additional_request_params:
            params_list = [f"{key}={value}" for key, value in self.additional_request_params.items()]
            params_request_str = f"&{'&'.join(params_list)}"
            return params_request_str
        return ""

    @property
    def report_request_body(self) -> str:
        if len(self.resource_ids) == 1:
            url = f"https://api.spotify.com/v1/{self.endpoint.value}/{self.resource_ids[0]}{self.additional_request_params_str}"
            return url
        
        url = f"https://api.spotify.com/v1/{self.endpoint.value}?ids={'%2C'.join(self.resource_ids)}{self.additional_request_params_str}"
        return url
