const StatsCards = ({ logsCount, alertsCount, detectionRate, severityCounts = {}, healthScore, onSeverityClick }) => {
  const getHealthStatus = (score) => {
    if (score >= 80) return { text: 'Secure', color: '#51cf66' };
    if (score >= 60) return { text: 'Stable', color: '#ffa500' };
    return { text: 'At Risk', color: '#ff6b6b' };
  };

  const health = getHealthStatus(healthScore || 50);

  return (
    <>
      <div className="stats-header">
        <h3>Network Overview</h3>
        <p>Real-time monitoring of network sessions and anomalies</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card primary">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h4>Total Logs</h4>
            <p className="stat-label">Sessions Processed</p>
            <p className="stat-number">{logsCount.toLocaleString()}</p>
          </div>
        </div>

        <div className="stat-card critical">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <h4>Anomalies</h4>
            <p className="stat-label">Detected & Logged</p>
            <p className="stat-number">{alertsCount.toLocaleString()}</p>
          </div>
        </div>

        <div className="stat-card success">
          <div className="stat-icon">📈</div>
          <div className="stat-content">
            <h4>Detection Rate</h4>
            <p className="stat-label">Anomalies vs Total</p>
            <p className="stat-number">{detectionRate.toFixed(2)}%</p>
          </div>
        </div>

        <div className="stat-card health">
          <div className="stat-icon">💚</div>
          <div className="stat-content">
            <h4>Network Health</h4>
            <p className="stat-label">{health.text}</p>
            <div className="health-bar">
              <div className="health-fill" style={{ width: `${healthScore || 50}%`, backgroundColor: health.color }} />
            </div>
            <p className="health-score">{healthScore || 50}%</p>
          </div>
        </div>
      </div>

      {(severityCounts.HIGH > 0 || severityCounts.MEDIUM > 0 || severityCounts.LOW > 0) && (
        <div className="severity-distribution">
          <h4>Threat Breakdown by Severity</h4>
          <div className="severity-bars">
            {severityCounts.HIGH > 0 && (
              <div 
                className="severity-bar-item clickable"
                onClick={() => onSeverityClick && onSeverityClick('high')}
              >
                <div className="bar-label">
                  <span className="severity-dot high"></span>
                  <span>Critical</span>
                </div>
                <div className="bar-container">
                  <div className="bar-fill high" style={{ width: `${Math.min(100, (severityCounts.HIGH / (severityCounts.HIGH + severityCounts.MEDIUM + severityCounts.LOW)) * 100)}%` }}>
                    {severityCounts.HIGH}
                  </div>
                </div>
              </div>
            )}
            {severityCounts.MEDIUM > 0 && (
              <div 
                className="severity-bar-item clickable"
                onClick={() => onSeverityClick && onSeverityClick('medium')}
              >
                <div className="bar-label">
                  <span className="severity-dot medium"></span>
                  <span>Warning</span>
                </div>
                <div className="bar-container">
                  <div className="bar-fill medium" style={{ width: `${Math.min(100, (severityCounts.MEDIUM / (severityCounts.HIGH + severityCounts.MEDIUM + severityCounts.LOW)) * 100)}%` }}>
                    {severityCounts.MEDIUM}
                  </div>
                </div>
              </div>
            )}
            {severityCounts.LOW > 0 && (
              <div 
                className="severity-bar-item clickable"
                onClick={() => onSeverityClick && onSeverityClick('low')}
              >
                <div className="bar-label">
                  <span className="severity-dot low"></span>
                  <span>Info</span>
                </div>
                <div className="bar-container">
                  <div className="bar-fill low" style={{ width: `${Math.min(100, (severityCounts.LOW / (severityCounts.HIGH + severityCounts.MEDIUM + severityCounts.LOW)) * 100)}%` }}>
                    {severityCounts.LOW}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default StatsCards;
