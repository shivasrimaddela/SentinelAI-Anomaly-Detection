import time
import json
from flask import Response

class StreamingService:
    def __init__(self, alert_service, logs_path, interval=2):
        self.alert_service = alert_service
        self.logs_path = logs_path
        self.interval = interval

    def _get_total_logs_count(self):
        try:
            with open(self.logs_path, "r", encoding="utf-8") as f:
                return len(f.readlines())
        except Exception:
            return 0

    def stream_alerts(self):
        def generate():
            last_alert_count = 0
            while True:
                try:
                    total_logs = self._get_total_logs_count()
                    alerts_count = self.alert_service.get_alert_count()
                    detection_rate = round(
                        (alerts_count / total_logs) * 100, 2
                    ) if total_logs > 0 else 0.0

                    # Send stats
                    yield f"data: {json.dumps({
                        'type': 'stats',
                        'data': {
                            'total_logs': total_logs,
                            'alerts_count': alerts_count,
                            'detection_rate': detection_rate
                        }
                    })}\n\n"

                    # Send new alerts
                    if alerts_count > last_alert_count:
                        new_alerts = self.alert_service.get_recent_alerts(
                            limit=(alerts_count - last_alert_count)
                        )
                        for alert in new_alerts:
                            yield f"data: {json.dumps({'type': 'alert', 'data': alert})}\n\n"
                        last_alert_count = alerts_count

                    time.sleep(self.interval)
                except Exception as e:
                    print(f"SSE error: {e}")
                    time.sleep(self.interval)

        return Response(generate(), mimetype='text/event-stream')
