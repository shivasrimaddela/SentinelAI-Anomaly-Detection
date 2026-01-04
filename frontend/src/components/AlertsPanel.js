import React from 'react';

const AlertsPanel = ({ alerts }) => {
  return (
    <div className="alerts-panel">
      <div className="panel-header">
        <h2>🚨 Recent Alerts</h2>
      </div>

      <div className="alerts-list">
        {alerts.length === 0 ? (
          <div className="empty-state">No alerts found</div>
        ) : (
          alerts.map((alert, index) => (
            <div
              key={index}
              className={`alert-item severity-${alert.severity?.toLowerCase()}`}
            >
              <div className="alert-header">
                <span className="severity-badge">
                  {alert.severity}
                </span>
                <span className="alert-time">
                  {new Date(alert.timestamp).toLocaleString()}
                </span>
              </div>
              <div className="alert-message">{alert.log}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default AlertsPanel;
