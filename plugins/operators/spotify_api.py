from airflow.models import BaseOperator

from enum import Enum


class Endpoint(Enum):
    pass


class SpotifyToGCSOperator(BaseOperator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    pass

    #def execute(self, endpoint: Endpoint, context: Context):
       # pass
