from django.conf import settings
from google.cloud import bigquery
from events_emitter.events_factory.base_time_series import BaseTimeSeries


class BigQueryTimeSeries(BaseTimeSeries):
    def get_event_last_creation(self, event_type, **kwargs):
        client = bigquery.Client()
        table_name = settings.TABLE_NAME
        query = client.query(f"SELECT created_at FROM `{table_name}` where event_type='{event_type}';")
        return query.result()
