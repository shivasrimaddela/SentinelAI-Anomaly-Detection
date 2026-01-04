const StatsCards = ({ logsCount, alertsCount, detectionRate }) => {
  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-icon">📊</div>
        <div className="stat-content">
          <h3>Total Logs</h3>
          <p className="stat-number">{logsCount}</p>
        </div>
      </div>

      <div className="stat-card alert">
        <div className="stat-icon">⚠️</div>
        <div className="stat-content">
          <h3>Anomalies Detected</h3>
          <p className="stat-number">{alertsCount}</p>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon">📈</div>
        <div className="stat-content">
          <h3>Detection Rate</h3>
          <p className="stat-number">{detectionRate}%</p>
        </div>
      </div>
    </div>
  );
};

export default StatsCards;
