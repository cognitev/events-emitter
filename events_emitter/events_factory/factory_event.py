from events_emitter.events_factory.bigquery_time_series import BigQueryTimeSeries


class FactoryEvent():
    @classmethod
    def create_event_class(cls, time_series_datastore):
        if not time_series_datastore or time_series_datastore == '':
            return BigQueryTimeSeries()
        elif time_series_datastore == 'bigquery':
            return BigQueryTimeSeries()
