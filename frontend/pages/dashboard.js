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
  flex: '1 1 180px',
});
const metricLabel = { fontSize: '0.75rem', color: '#555', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.3rem' };
const metricValue = { fontSize: '1.5rem', fontWeight: '700', color: '#0077b6' };

export default function DashboardPage() {
  const router = useRouter();
  const [checkups, setCheckups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dateFilter, setDateFilter] = useState('ALL'); // 'ALL', '30D', '90D'

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
        <h1>📊 Health Analytics Dashboard</h1>
        <Card><p style={{ color: '#888' }}>Loading your health records and trends…</p></Card>
      </Layout>
    );
  }

  if (checkups.length === 0) {
    return (
      <Layout>
        <h1>📊 Health Analytics Dashboard</h1>
        <Card>
          <div style={{ textAlign: 'center', padding: '2rem 0' }}>
            <p style={{ fontSize: '1.1rem', color: '#64748b', marginBottom: '1.25rem' }}>
              No health checkup records found. Complete your first assessment to unlock interactive dashboards.
            </p>
            <Link href="/healthcheck">
              <button className="btn-primary">Start Health Assessment →</button>
            </Link>
          </div>
        </Card>
      </Layout>
    );
  }

  // Filter checkups by date if requested
  const now = new Date();
  const filteredCheckups = checkups.filter((c) => {
    if (dateFilter === 'ALL') return true;
    const checkupDate = new Date(c.date);
    const diffDays = (now - checkupDate) / (1000 * 60 * 60 * 24);
    if (dateFilter === '30D') return diffDays <= 30;
    if (dateFilter === '90D') return diffDays <= 90;
    return true;
  });

  const displayCheckups = filteredCheckups.length > 0 ? filteredCheckups : checkups;
  const latest = checkups[checkups.length - 1];
  const latestDate = new Date(latest.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

  // Dates & chart tracks (chronological)
  const dates = displayCheckups.map((c) => new Date(c.date).toLocaleDateString([], { month: 'short', day: 'numeric' }));
  const bmis = displayCheckups.map((c) => c.bmi);
  const heartRates = displayCheckups.map((c) => c.heart_rate);
  const sleepHours = displayCheckups.map((c) => c.sleep_hours);
  const waterIntakes = displayCheckups.map((c) => c.water_intake);

  // Systolic / Diastolic tracks
  const systolics = displayCheckups.map((c) => {
    if (c.systolic) return c.systolic;
    if (c.blood_pressure && c.blood_pressure.includes('/')) {
      const parts = c.blood_pressure.split('/');
      return Number(parts[0]) || null;
    }
    return null;
  });
  const diastolics = displayCheckups.map((c) => {
    if (c.diastolic) return c.diastolic;
    if (c.blood_pressure && c.blood_pressure.includes('/')) {
      const parts = c.blood_pressure.split('/');
      return Number(parts[1]?.split(' ')[0]) || null;
    }
    return null;
  });

  return (
    <Layout>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ margin: 0 }}>📊 Health Analytics Dashboard</h1>
          <p style={{ color: '#64748b', margin: '0.25rem 0 0 0' }}>
            Latest Assessment: <strong>{latestDate}</strong> ({checkups.length} total assessments recorded)
          </p>
        </div>

        {/* Date Filter Buttons */}
        <div style={{ display: 'flex', gap: '0.5rem', background: '#e2e8f0', padding: '0.25rem', borderRadius: '8px' }}>
          {[
            { key: 'ALL', label: 'All Records' },
            { key: '90D', label: 'Last 90 Days' },
            { key: '30D', label: 'Last 30 Days' },
          ].map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setDateFilter(key)}
              style={{
                background: dateFilter === key ? '#0077b6' : 'transparent',
                color: dateFilter === key ? '#fff' : '#475569',
                border: 'none',
                borderRadius: '6px',
                padding: '0.4rem 0.8rem',
                fontSize: '0.8rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Primary Metrics */}
      <Card>
        <h2 style={{ fontSize: '1.1rem', marginBottom: '1rem', color: '#1e293b' }}>Latest Clinical Summary</h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={metricBox('#dff5ff')}>
            <div style={metricLabel}>BMI</div>
            <div style={metricValue}>{latest.bmi?.toFixed(1) ?? '—'}</div>
            <div style={{ fontSize: '0.8rem', color: '#0369a1', fontWeight: 600, marginTop: '0.25rem' }}>
              {latest.bmi < 18.5 ? 'Underweight' : latest.bmi < 25 ? 'Normal Weight' : latest.bmi < 30 ? 'Overweight' : 'Obesity'}
            </div>
          </div>
          <div style={metricBox('#fee2e2')}>
            <div style={metricLabel}>Resting Heart Rate</div>
            <div style={{ ...metricValue, color: '#dc2626' }}>{latest.heart_rate ?? '—'} bpm</div>
            <div style={{ fontSize: '0.8rem', color: '#991b1b', fontWeight: 600, marginTop: '0.25rem' }}>
              {latest.heart_rate >= 60 && latest.heart_rate <= 100 ? 'Normal Resting' : 'Review Advised'}
            </div>
          </div>
          <div style={metricBox('#fef3c7')}>
            <div style={metricLabel}>Blood Pressure</div>
            <div style={{ ...metricValue, color: '#d97706' }}>{latest.blood_pressure ?? '—'}</div>
            <div style={{ fontSize: '0.8rem', color: '#b45309', fontWeight: 600, marginTop: '0.25rem' }}>
              Systolic / Diastolic
            </div>
          </div>
          <div style={metricBox('#dcfce7')}>
            <div style={metricLabel}>Body Temperature</div>
            <div style={{ ...metricValue, color: '#16a34a' }}>{latest.temperature ?? '—'}°C</div>
            <div style={{ fontSize: '0.8rem', color: '#15803d', fontWeight: 600, marginTop: '0.25rem' }}>
              {latest.temperature >= 36.5 && latest.temperature <= 37.5 ? 'Normal Range' : 'Outside Reference'}
            </div>
          </div>
        </div>
      </Card>

      {/* Lifestyle Metrics */}
      <Card>
        <h2 style={{ fontSize: '1.1rem', marginBottom: '1rem', color: '#1e293b' }}>Lifestyle & Habit Indicators</h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={metricBox('#f3e8ff')}>
            <div style={metricLabel}>Sleep Duration</div>
            <div style={{ ...metricValue, color: '#9333ea' }}>{latest.sleep_hours ?? '—'} hrs</div>
            <div style={{ fontSize: '0.75rem', color: '#7e22ce' }}>Recommended: 7 - 9 hrs</div>
          </div>
          <div style={metricBox('#e0e7ff')}>
            <div style={metricLabel}>Weekly Exercise</div>
            <div style={{ ...metricValue, color: '#4f46e5' }}>{latest.exercise_days ?? '—'} days</div>
            <div style={{ fontSize: '0.75rem', color: '#4338ca' }}>Recommended: 3 - 5 days</div>
          </div>
          <div style={metricBox('#cffafe')}>
            <div style={metricLabel}>Hydration</div>
            <div style={{ ...metricValue, color: '#0891b2' }}>{latest.water_intake ?? '—'} glasses</div>
            <div style={{ fontSize: '0.75rem', color: '#0e7490' }}>Target: 8+ glasses</div>
          </div>
          <div style={metricBox('#f1f5f9')}>
            <div style={metricLabel}>Stress Level</div>
            <div style={{ ...metricValue, color: '#475569' }}>{latest.stress_level ?? 'Moderate'}</div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Self-Reported</div>
          </div>
        </div>
      </Card>

      {/* Interactive Charts */}
      <Card>
        <h2 style={{ fontSize: '1.1rem', marginBottom: '1rem', color: '#1e293b' }}>📈 Longitudinal Health Trends</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>
          {/* BMI Trend */}
          <div>
            <Plot
              data={[
                {
                  x: dates,
                  y: bmis,
                  type: 'scatter',
                  mode: 'lines+markers',
                  marker: { color: '#0077b6', size: 8 },
                  line: { color: '#0077b6', width: 3 },
                  name: 'BMI',
                },
              ]}
              layout={{
                title: 'BMI Progression',
                autosize: true,
                height: 280,
                margin: { t: 40, r: 20, l: 40, b: 40 },
                xaxis: { title: 'Assessment Date' },
                yaxis: { title: 'BMI (kg/m²)' },
              }}
              useResizeHandler
              style={{ width: '100%' }}
            />
          </div>

          {/* Blood Pressure Trend */}
          <div>
            <Plot
              data={[
                {
                  x: dates,
                  y: systolics,
                  type: 'scatter',
                  mode: 'lines+markers',
                  marker: { color: '#dc2626', size: 7 },
                  line: { color: '#dc2626', width: 2 },
                  name: 'Systolic',
                },
                {
                  x: dates,
                  y: diastolics,
                  type: 'scatter',
                  mode: 'lines+markers',
                  marker: { color: '#2563eb', size: 7 },
                  line: { color: '#2563eb', width: 2, dash: 'dot' },
                  name: 'Diastolic',
                },
              ]}
              layout={{
                title: 'Blood Pressure Tracking (mmHg)',
                autosize: true,
                height: 280,
                margin: { t: 40, r: 20, l: 40, b: 40 },
                xaxis: { title: 'Assessment Date' },
                yaxis: { title: 'Pressure (mmHg)' },
              }}
              useResizeHandler
              style={{ width: '100%' }}
            />
          </div>

          {/* Heart Rate Tracking */}
          <div>
            <Plot
              data={[
                {
                  x: dates,
                  y: heartRates,
                  type: 'scatter',
                  mode: 'lines+markers',
                  marker: { color: '#e11d48', size: 7 },
                  line: { color: '#e11d48', width: 2 },
                  name: 'Heart Rate',
                },
              ]}
              layout={{
                title: 'Resting Heart Rate (bpm)',
                autosize: true,
                height: 280,
                margin: { t: 40, r: 20, l: 40, b: 40 },
                xaxis: { title: 'Assessment Date' },
                yaxis: { title: 'BPM' },
              }}
              useResizeHandler
              style={{ width: '100%' }}
            />
          </div>

          {/* Lifestyle Tracking */}
          <div>
            <Plot
              data={[
                {
                  x: dates,
                  y: sleepHours,
                  type: 'bar',
                  marker: { color: '#a855f7' },
                  name: 'Sleep (hrs)',
                },
                {
                  x: dates,
                  y: waterIntakes,
                  type: 'bar',
                  marker: { color: '#06b6d4' },
                  name: 'Water (glasses)',
                },
              ]}
              layout={{
                title: 'Sleep & Hydration Habits',
                barmode: 'group',
                autosize: true,
                height: 280,
                margin: { t: 40, r: 20, l: 40, b: 40 },
                xaxis: { title: 'Assessment Date' },
                yaxis: { title: 'Units / Day' },
              }}
              useResizeHandler
              style={{ width: '100%' }}
            />
          </div>
        </div>

        <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem', justifyContent: 'flex-end', flexWrap: 'wrap' }}>
          <button onClick={() => router.push('/history')} className="btn-primary" style={{ padding: '0.6rem 1.2rem', fontSize: '0.9rem' }}>
            📂 Compare Assessments in History →
          </button>
          <button onClick={() => router.push('/reports')} style={{ padding: '0.6rem 1.2rem', fontSize: '0.9rem', background: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '8px', cursor: 'pointer', fontWeight: 600 }}>
            📄 Download Health Reports
          </button>
        </div>
      </Card>
    </Layout>
  );
}
