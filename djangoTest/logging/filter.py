import logging


class WorkerFilter(logging.Filter):
    def filter(self, record):
        return not getattr(record, 'is_staff', True)
