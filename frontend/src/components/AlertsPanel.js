import React, { useState } from 'react';

const generateImpactText = (alert) => {
  const severity = (alert.severity || 'UNKNOWN').toUpperCase();
  const message = (alert.log || '').toLowerCase();

  switch (severity) {
    case 'HIGH':
      if (message.includes('ddos') || message.includes('packet rate'))
        return 'Possible DDoS attack or data exfiltration attempt. Immediate investigation recommended.';
      if (message.includes('high-risk port'))
        return 'Suspicious remote access attempt to administrative services detected.';
      if (message.includes('retransmission spike'))
        return 'Network experiencing critical instability or active attack interference.';
      return 'Critical threat detected. Network security may be compromised.';

    case 'MEDIUM':
      if (message.includes('moderate packet rate'))
        return 'Elevated network activity detected. Monitor for patterns.';
      if (message.includes('unusual high port'))
        return 'Non-standard port communication detected. Could be legitimate or suspicious.';
      if (message.includes('retransmission'))
        return 'Network quality issues or intermittent connection problems.';
      return 'Suspicious activity pattern detected that warrants investigation.';

    case 'LOW':
      return 'Minor anomaly detected. Likely benign but worth noting in logs.';

    default:
      return 'Anomaly detected by hybrid ML + rule-based detection system.';
  }
};

const getSeverityBgColor = (severity) => {
  const level = (severity || 'UNKNOWN').toUpperCase();
  switch (level) {
    case 'HIGH':
      return '#ffe0e0';
    case 'MEDIUM':
      return '#fff4e0';
    case 'LOW':
      return '#e8f5e9';
    default:
      return '#f5f5f5';
  }
};

const AlertsPanel = ({ alerts, activeFilter, onFilterChange, filterOptions, severityCounts, onSeverityClick }) => {
  const [expandedAlert, setExpandedAlert] = useState(null);

  const activeSeverities = ['HIGH', 'MEDIUM', 'LOW'].filter(
    (level) => severityCounts[level] > 0 || activeFilter !== 'All'
  );

  const parseAlertDetails = (alert) => {
    const metadata = alert.metadata || {};
    return {
      src_ip: metadata.src_ip || 'N/A',
      dst_ip: metadata.dst_ip || 'N/A',
      protocol: metadata.protocol || 'Unknown',
      reason: alert.log || 'Anomaly detected',
      method: metadata.method || 'ML+Rules'
    };
  };

  return (
    <div className="alerts-panel">
      <div className="panel-header">
        <div className="panel-title">
          <h2>🚨 Security Alerts</h2>
          <p className="panel-subtitle">
            {alerts.length === 0
              ? '✅ No threats detected'
              : `${alerts.length} anomal${alerts.length === 1 ? 'y' : 'ies'} detected`}
          </p>
        </div>

        <div className="filter-section">
          <div className="filter-buttons">
            {filterOptions.map((level) => (
              <button
                key={level}
                className={`filter-btn ${activeFilter === level ? 'active' : ''}`}
                onClick={() => onFilterChange(level)}
                title={level === 'All' ? 'Show all alerts' : `${level}: ${severityCounts[level]} alerts`}
              >
                {level === 'All' ? '📊 All' : level}
                {level !== 'All' && severityCounts[level] > 0 && ` (${severityCounts[level]})`}
              </button>
            ))}
          </div>
        </div>
      </div>

      {activeSeverities.length > 0 && (
        <div className="severity-summary">
          <div className="summary-row">
            {activeSeverities.map((level) => (
              <div 
                key={level} 
                className={`summary-item severity-${level.toLowerCase()} clickable`}
                onClick={() => onSeverityClick && onSeverityClick(level.toLowerCase())}
              >
                <span className="count">{severityCounts[level]}</span>
                <span className="label">{level}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="alerts-list">
        {alerts.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">✅</div>
            <h4>Network Secure</h4>
            <p>No anomalies detected. Your network is operating normally.</p>
          </div>
        ) : (
          alerts.map((alert, index) => {
            const details = parseAlertDetails(alert);
            const severity = (alert.severity || 'UNKNOWN').toUpperCase();
            const isExpanded = expandedAlert === index;

            return (
              <div
                key={index}
                className={`alert-item severity-${severity.toLowerCase()}`}
                style={{ backgroundColor: getSeverityBgColor(severity) }}
              >
                <div className="alert-top">
                  <div className="alert-severity">
                    <span className={`severity-badge-lg severity-${severity.toLowerCase()}`}>
                      {severity === 'HIGH' ? '🔴' : severity === 'MEDIUM' ? '🟠' : '🟢'}
                      {' '}{severity}
                    </span>
                  </div>
                  <div className="alert-time">
                    {alert.timestamp ? new Date(alert.timestamp).toLocaleTimeString() : 'No timestamp'}
                  </div>
                </div>

                <div className="alert-network-info">
                  <div className="network-item">
                    <span className="label">Source IP:</span>
                    <span className="value mono">{details.src_ip}</span>
                  </div>
                  <span className="arrow">→</span>
                  <div className="network-item">
                    <span className="label">Destination IP:</span>
                    <span className="value mono">{details.dst_ip}</span>
                  </div>
                  <div className="network-item">
                    <span className="label">Protocol:</span>
                    <span className="value">{details.protocol}</span>
                  </div>
                </div>

                <div className="alert-reason-box">
                  <div className="reason-label">What Happened:</div>
                  <div className="reason-text">{details.reason}</div>
                </div>

                <div className="alert-impact-box" style={{ borderLeftColor: `#${severity === 'HIGH' ? 'ff6b6b' : severity === 'MEDIUM' ? 'ffa500' : '51cf66'}` }}>
                  <div className="impact-label">⚡ Impact & Severity:</div>
                  <div className="impact-text">{generateImpactText(alert)}</div>
                </div>

                {alert.metadata && (
                  <div className="alert-meta-footer">
                    <span className="meta-item">
                      🔬 Detection: <strong>{alert.metadata.method || 'Hybrid'}</strong>
                    </span>
                    {alert.metadata.ml_score !== undefined && (
                      <span className="meta-item">
                        📊 ML Score: <strong>{Math.abs(alert.metadata.ml_score).toFixed(3)}</strong>
                      </span>
                    )}
                  </div>
                )}

                <button
                  className="expand-btn"
                  onClick={() => setExpandedAlert(isExpanded ? null : index)}
                >
                  {isExpanded ? '▼ Less Details' : '▶ More Details'}
                </button>

                {isExpanded && alert.metadata?.rules && (
                  <div className="alert-details">
                    <h5>Detection Rules Triggered:</h5>
                    <ul>
                      {alert.metadata.rules.map((rule, i) => (
                        <li key={i}>{rule}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default AlertsPanel;

