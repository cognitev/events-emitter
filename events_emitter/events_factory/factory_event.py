from events_emitter.events_factory.bigquery_time_series import BigQueryTimeSeries


class FactoryEvent():
    @classmethod
    def create_event_class(cls, time_series_type):
        if not time_series_type or time_series_type == '':
            return BigQueryTimeSeries()
        elif time_series_type == 'bigquery':
            return BigQueryTimeSeries()
