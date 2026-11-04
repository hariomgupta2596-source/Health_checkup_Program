import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import dynamic from 'next/dynamic';
import Link from 'next/link';
import Layout from '../components/Layout';
import Card from '../components/Card';
import api from '../utils/api';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

const metricBox = (bg) => ({
  background: bg || '#e6f7ff',
  borderRadius: '10px',
  padding: '1rem 1.25rem',
  textAlign: 'center',
  flex: 1,
  minWidth: '130px',
});
const metricLabel = { fontSize: '0.75rem', color: '#555', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.3rem' };
const metricValue = { fontSize: '1.5rem', fontWeight: '700', color: '#0077b6' };

export default function DashboardPage() {
  const router = useRouter();
  const [checkups, setCheckups] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    if (!userId) { router.push('/login'); return; }
    api.get('/api/dashboard')
      .then((res) => setCheckups(res.data))
      .catch(() => setCheckups([]))
      .finally(() => setLoading(false));
  }, [router]);

  if (loading) {
    return (
      <Layout>
        <h1>📊 Dashboard</h1>
        <Card><p style={{ color: '#888' }}>Loading your health data…</p></Card>
      </Layout>
    );
  }

  if (checkups.length === 0) {
    return (
      <Layout>
        <h1>📊 Dashboard</h1>
        <Card>
          <p style={{ color: '#888', marginBottom: '1rem' }}>No checkup data yet.</p>
          <Link href="/healthcheck">
            <button className="btn-primary">Start your first checkup →</button>
          </Link>
        </Card>
      </Layout>
    );
  }

  const latest = checkups[0];
  const latestDate = new Date(latest.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

  // Chart data (oldest first)
  const ordered = [...checkups].reverse();
  const dates = ordered.map((c) => new Date(c.date).toLocaleDateString());
  const bmis = ordered.map((c) => c.bmi);
  const bps = ordered.map((c) => c.blood_pressure || '');

  return (
    <Layout>
      <h1>📊 Dashboard</h1>
      <p style={{ color: '#888', marginBottom: '1.25rem' }}>Latest checkup: <strong>{latestDate}</strong></p>

      {/* Primary metrics */}
      <Card>
        <h2 style={{ marginBottom: '1rem' }}>Latest Health Metrics</h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={metricBox('#dff5ff')}>
            <div style={metricLabel}>BMI</div>
            <div style={metricValue}>{latest.bmi?.toFixed(1) ?? '—'}</div>
          </div>
          <div style={metricBox('#fce8e8')}>
            <div style={metricLabel}>Heart Rate</div>
            <div style={{ ...metricValue, color: '#c0392b' }}>{latest.heart_rate ?? '—'} bpm</div>
          </div>
          <div style={metricBox('#e8f8e8')}>
            <div style={metricLabel}>Temperature</div>
            <div style={{ ...metricValue, color: '#27ae60' }}>{latest.temperature ?? '—'}°C</div>
          </div>
          <div style={metricBox('#fff8e1')}>
            <div style={metricLabel}>Blood Pressure</div>
            <div style={{ ...metricValue, color: '#e67e22' }}>{latest.blood_pressure ?? '—'}</div>
          </div>
        </div>
      </Card>

      {/* Lifestyle metrics */}
      <Card>
        <h2 style={{ marginBottom: '1rem' }}>Lifestyle Overview</h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={metricBox('#f0e6ff')}>
            <div style={metricLabel}>Sleep</div>
            <div style={{ ...metricValue, color: '#8e44ad' }}>{latest.sleep_hours ?? '—'} hrs</div>
          </div>
          <div style={metricBox('#e6ffe6')}>
            <div style={metricLabel}>Exercise</div>
            <div style={{ ...metricValue, color: '#27ae60' }}>{latest.exercise_days ?? '—'} days/wk</div>
          </div>
          <div style={metricBox('#e6f7ff')}>
            <div style={metricLabel}>Water Intake</div>
            <div style={metricValue}>{latest.water_intake ?? '—'} glasses</div>
          </div>
        </div>
      </Card>

      {/* BMI Trend Chart */}
      {checkups.length > 1 && (
        <Card>
          <h2 style={{ marginBottom: '1rem' }}>BMI Trend Over Time</h2>
          <Plot
            data={[
              {
                x: dates,
                y: bmis,
                type: 'scatter',
                mode: 'lines+markers',
                marker: { color: '#0077b6' },
                line: { color: '#0077b6' },
                name: 'BMI',
              },
            ]}
            layout={{
              autosize: true,
              margin: { t: 20, r: 20, l: 50, b: 50 },
              yaxis: { title: 'BMI' },
              xaxis: { title: 'Date' },
              paper_bgcolor: 'transparent',
              plot_bgcolor: '#f8fbff',
            }}
            style={{ width: '100%', height: '300px' }}
            config={{ responsive: true, displayModeBar: false }}
          />
        </Card>
      )}

      {/* Blood Pressure Trend Chart */}
      {checkups.length > 1 && (
        <Card>
          <h2 style={{ marginBottom: '1rem' }}>Blood Pressure Over Time</h2>
          <Plot
            data={[
              {
                x: dates,
                y: bps,
                type: 'scatter',
                mode: 'lines+markers',
                marker: { color: '#e74c3c' },
                line: { color: '#e74c3c' },
                name: 'Blood Pressure',
              },
            ]}
            layout={{
              autosize: true,
              margin: { t: 20, r: 20, l: 50, b: 50 },
              yaxis: { title: 'Blood Pressure' },
              xaxis: { title: 'Date' },
              paper_bgcolor: 'transparent',
              plot_bgcolor: '#fff8f8',
            }}
            style={{ width: '100%', height: '300px' }}
            config={{ responsive: true, displayModeBar: false }}
          />
        </Card>
      )}

      {/* History table */}
      <Card>
        <h2 style={{ marginBottom: '1rem' }}>Checkup History</h2>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ background: '#e6f7ff' }}>
                {['Date', 'BMI', 'Heart Rate', 'Temp (°C)', 'Blood Pressure', 'Sleep', 'Exercise', 'Water'].map((h) => (
                  <th key={h} style={{ padding: '0.6rem 0.75rem', textAlign: 'left', color: '#0077b6' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {checkups.map((c, i) => (
                <tr key={c.id} style={{ background: i % 2 === 0 ? '#fff' : '#f8fbff' }}>
                  <td style={{ padding: '0.5rem 0.75rem' }}>{new Date(c.date).toLocaleDateString()}</td>
                  <td style={{ padding: '0.5rem 0.75rem' }}>{c.bmi?.toFixed(1)}</td>
                  <td style={{ padding: '0.5rem 0.75rem' }}>{c.heart_rate}</td>
                  <td style={{ padding: '0.5rem 0.75rem' }}>{c.temperature}</td>
                  <td style={{ padding: '0.5rem 0.75rem' }}>{c.blood_pressure}</td>
                  <td style={{ padding: '0.5rem 0.75rem' }}>{c.sleep_hours}</td>
                  <td style={{ padding: '0.5rem 0.75rem' }}>{c.exercise_days}</td>
                  <td style={{ padding: '0.5rem 0.75rem' }}>{c.water_intake}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </Layout>
  );
}
