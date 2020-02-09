from abc import ABC, abstractmethod


class BaseTimeSeries(ABC):
    @abstractmethod
    def get_event_last_creation(self, event_type, **kwargs):
        pass
