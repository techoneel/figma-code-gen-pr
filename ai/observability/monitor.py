# Observability Monitor

import datetime

class Monitor:
    def track(self, event: str, data: dict = None):
        timestamp = datetime.datetime.utcnow().isoformat()
        print({
            "timestamp": timestamp,
            "event": event,
            "data": data or {}
        })
