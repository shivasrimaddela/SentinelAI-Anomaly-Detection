from flask import Blueprint
from src.services.streaming_service import StreamingService
from src.services.alert_service import AlertService
from src.config import ALERT_LOG_PATH, LOG_PATH, STREAM_INTERVAL

stream_bp = Blueprint('stream', __name__)

@stream_bp.route('/stream/alerts', methods=['GET'])
def stream_alerts():
    alert_service = AlertService(ALERT_LOG_PATH)
    streaming_service = StreamingService(
        alert_service=alert_service,
        logs_path=LOG_PATH,
        interval=STREAM_INTERVAL
    )
    return streaming_service.stream_alerts()
