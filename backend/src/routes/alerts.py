from flask import Blueprint, jsonify
from src.services.alert_service import AlertService
from src.config import ALERT_LOG_PATH

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/alerts', methods=['GET'])
def get_alerts():
    alert_service = AlertService(ALERT_LOG_PATH)
    alerts = alert_service.get_recent_alerts(limit=100)
    return jsonify({'alerts': alerts, 'count': len(alerts)})

@alerts_bp.route('/alerts/count', methods=['GET'])
def get_alert_count():
    alert_service = AlertService(ALERT_LOG_PATH)
    count = alert_service.get_alert_count()
    return jsonify({'count': count})
