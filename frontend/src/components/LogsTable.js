import React, { useState, useMemo } from 'react';

const LogsTable = ({ logs }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [searchIP, setSearchIP] = useState('');
  const [filterType, setFilterType] = useState('All');
  const logsPerPage = 10;

  const parseLog = (logObj) => {
    const parts = (logObj.raw || '').split(',');

    return {
      timestamp: parts[0] || logObj.timestamp || '',
      ip: parts[1] || logObj.source_ip || '',
      method: (parts[2] || logObj.method || 'N/A').toUpperCase(),
      status: parts[3] || logObj.status || 'Unknown',
      browser: parts[4] || logObj.browser || 'N/A',
      location: parts[5] || logObj.location || 'Unknown',
      action: parts[6] || logObj.action || logObj.event || 'Session',
      type: logObj.type || 'normal',
      severity: (logObj.severity || 'LOW').toUpperCase(),
    };
  };

  const filteredLogs = useMemo(() => {
    let result = logs.map(parseLog);

    if (searchIP) {
      result = result.filter((log) =>
        log.ip.toLowerCase().includes(searchIP.toLowerCase())
      );
    }

    if (filterType !== 'All') {
      result = result.filter((log) =>
        log.type === filterType.toLowerCase()
      );
    }

    return result;
  }, [logs, searchIP, filterType]);

  const indexOfLastLog = currentPage * logsPerPage;
  const indexOfFirstLog = indexOfLastLog - logsPerPage;
  const currentLogs = filteredLogs.slice(indexOfFirstLog, indexOfLastLog);
  const totalPages = Math.ceil(filteredLogs.length / logsPerPage);

  return (
    <div className="logs-table-container">
      <div className="table-controls">
        <div className="control-group">
          <h2>📋 Session Logs</h2>
          <p className="table-description">All network sessions processed by the system</p>
        </div>

        <div className="control-filters">
          <div className="search-box">
            <input
              type="text"
              placeholder="🔍 Search by IP address..."
              value={searchIP}
              onChange={(e) => {
                setSearchIP(e.target.value);
                setCurrentPage(1);
              }}
              className="search-input"
            />
          </div>

          <div className="type-filter">
            <select
              value={filterType}
              onChange={(e) => {
                setFilterType(e.target.value);
                setCurrentPage(1);
              }}
              className="filter-select"
            >
              <option value="All">All Sessions</option>
              <option value="Normal">Normal Only</option>
              <option value="Anomaly">Anomalies Only</option>
            </select>
          </div>
        </div>
      </div>

      <div className="table-stats">
        <span className="stat-item">Total: {filteredLogs.length}</span>
        <span className="stat-item">Page {currentPage} of {Math.max(1, totalPages)}</span>
      </div>

      <div className="table-wrapper">
        <table className="logs-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Source IP</th>
              <th>Action</th>
              <th>Severity</th>
              <th>Status</th>
              <th>Type</th>
            </tr>
          </thead>

          <tbody>
            {currentLogs.map((log, index) => {
              const isAnomaly = log.type === 'anomaly' || log.severity === 'HIGH';

              return (
                <tr key={index} className={isAnomaly ? 'row-anomaly' : ''}>
                  <td className="cell-time">
                    <span className="time-label">{log.timestamp.split(' ')[0]}</span>
                    <span className="time-value">{log.timestamp.split(' ')[1]}</span>
                  </td>
                  <td className="cell-ip">
                    <code>{log.ip}</code>
                  </td>
                  <td className="cell-action">{log.action}</td>
                  <td className="cell-severity">
                    <span className={`severity-tag severity-${log.severity.toLowerCase()}`}>
                      {log.severity === 'HIGH' ? '🔴' : log.severity === 'MEDIUM' ? '🟠' : '🟢'}
                      {' '}{log.severity}
                    </span>
                  </td>
                  <td className="cell-status">
                    <span className={`status-tag status-${log.status.charAt(0).toLowerCase()}`}>
                      {log.status}
                    </span>
                  </td>
                  <td className="cell-type">
                    {isAnomaly ? (
                      <span className="type-badge anomaly">
                        ⚠️ Anomaly
                      </span>
                    ) : (
                      <span className="type-badge normal">
                        ✓ Normal
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {currentLogs.length === 0 && (
          <div className="empty-table">
            <p>No logs match your search criteria</p>
          </div>
        )}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            className="pagination-btn"
            onClick={() => setCurrentPage(1)}
            disabled={currentPage === 1}
          >
            « First
          </button>
          <button
            className="pagination-btn"
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={currentPage === 1}
          >
            ‹ Previous
          </button>
          <span className="page-info">
            Page <strong>{currentPage}</strong> / {totalPages}
          </span>
          <button
            className="pagination-btn"
            onClick={() => setCurrentPage(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            Next ›
          </button>
          <button
            className="pagination-btn"
            onClick={() => setCurrentPage(totalPages)}
            disabled={currentPage === totalPages}
          >
            Last »
          </button>
        </div>
      )}
    </div>
  );
};

export default LogsTable;
