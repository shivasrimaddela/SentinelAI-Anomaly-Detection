import React from 'react';

const Header = ({ alertCount }) => {
  return (
    <header className="header">
      <div className="header-content">
        <h1>SentinelAI</h1>
        <div className="header-stats">
          <div className="stat-badge">
            <span className="stat-label">Total Alerts</span>
            <span className="stat-value">{alertCount || 0}</span>
          </div>
       </div>
      </div>
    </header>
  );
};

export default Header;
