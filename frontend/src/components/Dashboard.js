import React, { useState, useEffect, useMemo } from 'react';
import apiService from '../services/api';
import Header from './Header';
import StatsCards from './StatsCards';
import AlertsPanel from './AlertsPanel';
import LogsTable from './LogsTable';
import Loader from './Loader';

const DEFAULT_FILTER = 'All';
const ALERT_LEVELS = ['All', 'HIGH', 'MEDIUM', 'LOW'];

const Dashboard = () => {
  const [logs, setLogs] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [totalLogs, setTotalLogs] = useState(0);
  const [alertCount, setAlertCount] = useState(0);
  const [detectionRate, setDetectionRate] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState(DEFAULT_FILTER);
  const [streamActive, setStreamActive] = useState(false);
  const [healthStatus, setHealthStatus] = useState('checking');
  const [lastUpdate, setLastUpdate] = useState('never');
  const [activeView, setActiveView] = useState('dashboard');

  const severityCounts = useMemo(() => {
    return alerts.reduce(
      (acc, alert) => {
        const level = (alert.severity || 'UNKNOWN').toUpperCase();
        acc[level] = (acc[level] || 0) + 1;
        return acc;
      },
      { HIGH: 0, MEDIUM: 0, LOW: 0, UNKNOWN: 0 }
    );
  }, [alerts]);

  const filteredAlerts = useMemo(() => {
    if (filter === DEFAULT_FILTER) return alerts;
    return alerts.filter((alert) => (alert.severity || 'UNKNOWN') === filter);
  }, [alerts, filter]);

  const healthCheckScore = useMemo(() => {
    if (!streamActive) return 0;
    if (totalLogs === 0) return 30;
    if (alertCount === 0) return 90;
    return Math.min(95, Math.max(40, 100 - detectionRate * 2));
  }, [streamActive, totalLogs, alertCount, detectionRate]);

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [logsData, alertsData, healthData] = await Promise.all([
          apiService.getLogs(),
          apiService.getAlerts(),
          apiService.healthCheck().catch(() => ({ status: 'offline' }))
        ]);

        setLogs(logsData.logs || []);
        setTotalLogs(logsData.count || 0);
        setAlerts(alertsData.alerts || []);
        setAlertCount(alertsData.count || 0);
        setHealthStatus(healthData?.status === 'healthy' ? 'healthy' : 'warning');
        setLoading(false);
      } catch {
        setError('Backend not reachable - Check if Flask server is running on port 8000');
        setHealthStatus('offline');
        setLoading(false);
      }
    };

    loadInitialData();

    const es = new EventSource('http://localhost:8000/stream/alerts');

    es.onopen = () => {
      setStreamActive(true);
      setHealthStatus('healthy');
      setLastUpdate(new Date().toLocaleTimeString());
    };

    es.onerror = () => {
      setStreamActive(false);
      setHealthStatus('offline');
    };

    es.onmessage = (event) => {
      const msg = JSON.parse(event.data);

      if (msg.type === 'stats') {
        setTotalLogs(msg.data.total_logs);
        setAlertCount(msg.data.alerts_count);
        setDetectionRate(msg.data.detection_rate);
        setLastUpdate(new Date().toLocaleTimeString());
      }

      if (msg.type === 'alert') {
        setAlerts((prev) => [msg.data, ...prev]);
        setLastUpdate(new Date().toLocaleTimeString());
      }
    };

    return () => es.close();
  }, []);

  if (loading) return <Loader />;

  if (error) {
    return (
      <div className="error-container">
        <div className="error-icon">⚠️</div>
        <h2>Connection Error</h2>
        <p>{error}</p>
        <div className="error-help">
          <h4>📌 Troubleshooting Steps:</h4>
          <ul>
            <li>Make sure Flask backend is running: <code>python src/app.py</code></li>
            <li>Check if port 8000 is available</li>
            <li>Verify backend data paths in config.py</li>
            <li>Refresh this page after starting the backend</li>
          </ul>
        </div>
      </div>
    );
  }

  // Full-Screen Alert View
  if (activeView !== 'dashboard') {
    const severityType = activeView.toUpperCase();
    const severityAlerts = alerts.filter(
      (alert) => (alert.severity || 'UNKNOWN') === severityType
    );

    return (
      <div className="dashboard">
        <Header 
          alertCount={alertCount} 
          streamActive={streamActive}
          healthStatus={healthStatus}
          lastUpdate={lastUpdate}
        />

        <div className="container">
          <div className="fullscreen-alert-view">
            <div className="alert-view-header">
              <button 
                className="back-btn"
                onClick={() => setActiveView('dashboard')}
              >
                ← Back to Dashboard
              </button>
              <h2 className="alert-view-title">
                {severityType} Severity Alerts
              </h2>
              <div className="alert-view-count">
                {severityAlerts.length} alert{severityAlerts.length !== 1 ? 's' : ''}
              </div>
            </div>

            <div className="fullscreen-alerts-container">
              {severityAlerts.length === 0 ? (
                <div className="empty-alerts">
                  <div className="empty-icon">✓</div>
                  <h3>No {severityType} Severity Alerts</h3>
                  <p>Everything looks good for {severityType.toLowerCase()} severity threats!</p>
                </div>
              ) : (
                <div className="alerts-grid">
                  {severityAlerts.map((alert, idx) => (
                    <div 
                      key={idx} 
                      className={`fullscreen-alert-card severity-${(alert.severity || 'UNKNOWN').toLowerCase()}`}
                    >
                      <div className="card-header">
                        <span className="severity-badge">{alert.severity || 'UNKNOWN'}</span>
                        <span className="card-time">{alert.timestamp || 'N/A'}</span>
                      </div>

                      <div className="card-section network-section">
                        <h4 className="section-title">Network Information</h4>
                        <div className="network-grid">
                          <div className="network-field">
                            <label>Source IP</label>
                            <code>{alert.source_ip || 'N/A'}</code>
                          </div>
                          <div className="network-field">
                            <label>Destination IP</label>
                            <code>{alert.destination_ip || 'N/A'}</code>
                          </div>
                          <div className="network-field">
                            <label>Protocol</label>
                            <code>{alert.protocol || 'N/A'}</code>
                          </div>
                          <div className="network-field">
                            <label>Port</label>
                            <code>{alert.port || 'N/A'}</code>
                          </div>
                        </div>
                      </div>

                      <div className="card-section reason-section">
                        <h4 className="section-title">Alert Reason</h4>
                        <p className="reason-text">{alert.reason || 'Anomaly detected by system'}</p>
                      </div>

                      <div className="card-section details-section">
                        <h4 className="section-title">Details</h4>
                        <div className="details-grid">
                          <div className="detail-item">
                            <span className="detail-label">Detection Method:</span>
                            <span className="detail-value">{alert.ml_score ? 'ML Model' : 'Rule-Based'}</span>
                          </div>
                          {alert.ml_score && (
                            <div className="detail-item">
                              <span className="detail-label">ML Score:</span>
                              <span className="detail-value">{alert.ml_score.toFixed(3)}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Main Dashboard View
  return (
    <div className="dashboard">
      <Header 
        alertCount={alertCount} 
        streamActive={streamActive}
        healthStatus={healthStatus}
        lastUpdate={lastUpdate}
      />

      <div className="container">
        <StatsCards
          logsCount={totalLogs}
          alertsCount={alertCount}
          detectionRate={detectionRate}
          severityCounts={severityCounts}
          healthScore={healthCheckScore}
          onSeverityClick={setActiveView}
        />

        <div className="main-content">
          <AlertsPanel
            alerts={filteredAlerts}
            activeFilter={filter}
            onFilterChange={setFilter}
            filterOptions={ALERT_LEVELS}
            severityCounts={severityCounts}
            onSeverityClick={setActiveView}
          />
          <LogsTable logs={logs} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
