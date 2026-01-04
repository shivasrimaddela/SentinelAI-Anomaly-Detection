import React, { useState, useEffect } from 'react';
import apiService from '../services/api';
import Header from './Header';
import StatsCards from './StatsCards';
import AlertsPanel from './AlertsPanel';
import LogsTable from './LogsTable';
import Loader from './Loader';

const Dashboard = () => {
  const [logs, setLogs] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [totalLogs, setTotalLogs] = useState(0);
  const [alertCount, setAlertCount] = useState(0);
  const [detectionRate, setDetectionRate] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const logsData = await apiService.getLogs();
        setLogs(logsData.logs || []);
        setTotalLogs(logsData.count || 0);
        setLoading(false);
      } catch {
        setError('Backend not reachable');
        setLoading(false);
      }
    };

    loadInitialData();

    const es = new EventSource('http://localhost:8000/stream/alerts');

    es.onmessage = (event) => {
      const msg = JSON.parse(event.data);

      if (msg.type === 'stats') {
        setTotalLogs(msg.data.total_logs);
        setAlertCount(msg.data.alerts_count);
        setDetectionRate(msg.data.detection_rate);
      }

      if (msg.type === 'alert') {
        setAlerts((prev) => [msg.data, ...prev]);
      }
    };

    return () => es.close();
  }, []);

  if (loading) return <Loader />;

  if (error) {
    return (
      <div className="error-container">
        <h2>⚠️ Error</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <Header alertCount={alertCount} />

      <div className="container">
        <StatsCards
          logsCount={totalLogs}
          alertsCount={alertCount}
          detectionRate={detectionRate}
        />

        <div className="main-content">
          <AlertsPanel alerts={alerts} />
          <LogsTable logs={logs} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
