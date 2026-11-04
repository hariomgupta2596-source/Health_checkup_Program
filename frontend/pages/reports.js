import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import Card from '../components/Card';
import api from '../utils/api';

export default function ReportsPage() {
  const router = useRouter();
  const [latest, setLatest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    if (!userId) { router.push('/login'); return; }

    api.get('/api/reports/latest')
      .then((res) => setLatest(res.data))
      .catch((err) => {
        if (err.response?.status === 404) {
          setLatest(null);
        } else {
          setError('Failed to load report data.');
        }
      })
      .finally(() => setLoading(false));
  }, [router]);

  async function handleDownload() {
    if (!latest) return;
    setDownloading(true);
    setError('');
    try {
      const res = await api.get(`/api/reports/pdf/${latest.id}`, { responseType: 'blob' });
      const blob = new Blob([res.data], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `health_report_${latest.id}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to download PDF. Please try again.');
    } finally {
      setDownloading(false);
    }
  }

  return (
    <Layout>
      <h1>📄 Health Reports</h1>

      {loading && (
        <Card><p style={{ color: '#888' }}>Loading report data…</p></Card>
      )}

      {!loading && error && (
        <Card>
          <div style={{ color: '#e74c3c', background: '#fdf0f0', borderRadius: '8px', padding: '0.75rem 1rem' }}>
            {error}
          </div>
        </Card>
      )}

      {!loading && !error && !latest && (
        <Card>
          <p style={{ color: '#888', marginBottom: '1rem' }}>
            No checkup data found. Complete a health checkup first to generate a report.
          </p>
          <a href="/healthcheck">
            <button className="btn-primary">Go to Health Checkup →</button>
          </a>
        </Card>
      )}

      {!loading && latest && (
        <>
          <Card>
            <h2 style={{ marginBottom: '0.75rem' }}>Latest Checkup Report</h2>
            <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap', marginBottom: '1.25rem' }}>
              <div>
                <div style={{ fontSize: '0.8rem', color: '#888', marginBottom: '0.2rem' }}>Checkup ID</div>
                <div style={{ fontWeight: '700', fontSize: '1.1rem', color: '#0077b6' }}>#{latest.id}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: '#888', marginBottom: '0.2rem' }}>Date</div>
                <div style={{ fontWeight: '700', fontSize: '1.1rem', color: '#0077b6' }}>
                  {new Date(latest.date).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </div>
              </div>
            </div>

            <button
              className="btn-primary"
              onClick={handleDownload}
              disabled={downloading}
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
            >
              {downloading ? '⏳ Generating PDF…' : '📥 Download PDF Report'}
            </button>

            {error && (
              <div style={{ color: '#e74c3c', marginTop: '0.75rem', fontSize: '0.9rem' }}>{error}</div>
            )}
          </Card>

          <Card>
            <h2 style={{ marginBottom: '0.5rem' }}>About PDF Reports</h2>
            <ul style={{ paddingLeft: '1.25rem', lineHeight: '2', color: '#555' }}>
              <li>Includes all health metrics from your latest checkup</li>
              <li>Lists medical condition flags (diabetes, hypertension, etc.)</li>
              <li>Generated on-demand using your most recent data</li>
              <li>For educational purposes — not a medical document</li>
            </ul>
          </Card>
        </>
      )}
    </Layout>
  );
}
