import React, { useState } from 'react';

const LogsTable = ({ logs }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const logsPerPage = 10;

  const indexOfLastLog = currentPage * logsPerPage;
  const indexOfFirstLog = indexOfLastLog - logsPerPage;
  const currentLogs = logs.slice(indexOfFirstLog, indexOfLastLog);

  const totalPages = Math.ceil(logs.length / logsPerPage);

  const parseLog = (logObj) => {
    const parts = logObj.raw.split(',');

    return {
      timestamp: parts[0] || '',
      ip: parts[1] || '',
      method: parts[2] || '',
      status: parts[3] || '',
      browser: parts[4] || '',
      location: parts[5] || '',
      action: parts[6] || '',
      type: logObj.type || 'normal',
      severity: logObj.severity || null,
    };
  };

  return (
    <div className="logs-table-container">
      <h2>📋 Recent Logs</h2>

      <div className="table-wrapper">
        <table className="logs-table">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>IP Address</th>
            <th>Method</th>
            <th>Status</th>
            <th>Browser</th>
            <th>Location</th>
            <th>Action</th>
            <th>Type</th>
          </tr>
        </thead>

          <tbody>
            {currentLogs.map((logObj, index) => {
              const parsed = parseLog(logObj);

              return (
                <tr
                  key={index}
                  style={
                    parsed.type === 'anomaly'
                      ? { backgroundColor: '#fff5f5' }
                      : {}
                  }
                >
                  <td>{parsed.timestamp}</td>
                  <td className="mono">{parsed.ip}</td>
                  <td>
                    <span className={`method-badge ${parsed.method.toLowerCase()}`}>
                      {parsed.method}
                    </span>
                  </td>
                  <td>
                    <span className={`status-badge status-${parsed.status.charAt(0)}`}>
                      {parsed.status}
                    </span>
                  </td>
                  <td>{parsed.browser}</td>
                  <td>{parsed.location}</td>
                  <td>{parsed.action}</td>
                  <td>
                    {parsed.type === 'anomaly' ? '⚠️ Anomaly' : 'Normal'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span className="page-info">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default LogsTable;
