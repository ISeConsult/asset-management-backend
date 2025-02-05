from pythonjsonlogger import jsonlogger
from django.utils import timezone

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        
        if not log_record.get('timestamp'):
            now = timezone.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        
        log_record['level'] = log_record.get('level', record.levelname).upper()
        log_record['env'] = 'local'
