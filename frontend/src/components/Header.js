import React from 'react';

const Header = ({ alertCount, streamActive, healthStatus, lastUpdate }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return '#51cf66';
      case 'warning':
        return '#ffa500';
      case 'offline':
        return '#ff6b6b';
      default:
        return '#95a5a6';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'healthy':
        return 'System Healthy';
      case 'warning':
        return 'Elevated Activity';
      case 'offline':
        return 'Connection Lost';
      default:
        return 'Checking...';
    }
  };

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <div>
            <h1>🛡️ SentinelAI</h1>
            <p className="header-tagline">Real-time Wireshark-based network anomaly detection powered by ML</p>
          </div>
        </div>

        <div className="header-right">
          <div className="header-stats-grid">
            <div className="header-stat">
              <div className="stat-label">Total Alerts</div>
              <div className="stat-badge">{alertCount}</div>
            </div>

            <div className="header-stat">
              <div className="stat-label">Stream Status</div>
              <div className="stream-indicator" style={{ borderColor: streamActive ? '#51cf66' : '#ff6b6b' }}>
                <span className={`status-dot ${streamActive ? 'online' : 'offline'}`} />
                {streamActive ? 'Live' : 'Offline'}
              </div>
            </div>

            <div className="header-stat">
              <div className="stat-label">System Health</div>
              <div className="health-indicator" style={{ borderColor: getStatusColor(healthStatus) }}>
                <span className="status-dot" style={{ backgroundColor: getStatusColor(healthStatus) }} />
                {getStatusText(healthStatus)}
              </div>
            </div>

            <div className="header-stat">
              <div className="stat-label">Last Update</div>
              <div className="timestamp">{lastUpdate}</div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
