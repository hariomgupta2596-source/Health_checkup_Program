import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import Layout from '../components/Layout';
import Card from '../components/Card';
import api from '../utils/api';

const metricBoxStyle = {
  background: '#e6f7ff',
  borderRadius: '10px',
  padding: '1.25rem 1.5rem',
  textAlign: 'center',
  flex: 1,
  minWidth: '140px',
};

const metricLabelStyle = {
  fontSize: '0.8rem',
  color: '#555',
  textTransform: 'uppercase',
  letterSpacing: '0.05em',
  marginBottom: '0.4rem',
};

const metricValueStyle = {
  fontSize: '1.75rem',
  fontWeight: '700',
  color: '#0077b6',
};

export default function HomePage() {
  const [checkups, setCheckups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    if (userId) {
      setLoggedIn(true);
      api
        .get('/api/dashboard')
        .then((res) => setCheckups(res.data))
        .catch(() => setCheckups([]))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const today = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });

  return (
    <Layout>
      {/* Hero section */}
      <Card>
        <div
          style={{
            display: 'flex',
            gap: '2rem',
            alignItems: 'center',
            flexWrap: 'wrap',
          }}
        >
          <div style={{ flexShrink: 0 }}>
            <Image
              src="https://cdn-icons-png.flaticon.com/512/2491/2491939.png"
              alt="Health Checkup"
              width={200}
              height={200}
              style={{ borderRadius: '12px' }}
            />
          </div>
          <div style={{ flex: 1 }}>
            <h1 style={{ fontSize: '1.9rem', marginBottom: '0.75rem' }}>
              Welcome to Health Checkup Program 🏥
            </h1>
            <ul style={{ paddingLeft: '1.25rem', lineHeight: '2', color: '#555' }}>
              <li>📋 Comprehensive health assessments</li>
              <li>📊 Track your health metrics over time</li>
              <li>💡 Personalised recommendations</li>
              <li>📄 Downloadable PDF health reports</li>
              <li>📚 Evidence-based health guidelines</li>
            </ul>
            <Link href="/healthcheck">
              <button className="btn-primary" style={{ marginTop: '1.25rem' }}>
                Get Started →
              </button>
            </Link>
          </div>
        </div>
      </Card>

      {/* Stats row */}
      <Card>
        <h2 style={{ marginBottom: '1rem' }}>Your Health Overview</h2>
        {!loggedIn ? (
          <p style={{ color: '#888' }}>Please login to see your stats.</p>
        ) : loading ? (
          <p style={{ color: '#888' }}>Loading your stats…</p>
        ) : (
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            <div style={metricBoxStyle}>
              <div style={metricLabelStyle}>Total Checkups</div>
              <div style={metricValueStyle}>{checkups.length}</div>
            </div>
            <div style={metricBoxStyle}>
              <div style={metricLabelStyle}>Status</div>
              <div style={{ ...metricValueStyle, color: '#27ae60', fontSize: '1.4rem' }}>
                Active ✓
              </div>
            </div>
            <div style={metricBoxStyle}>
              <div style={metricLabelStyle}>Last Updated</div>
              <div style={{ ...metricValueStyle, fontSize: '1.1rem' }}>
                {checkups.length > 0
                  ? new Date(checkups[0].date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                    })
                  : today}
              </div>
            </div>
          </div>
        )}
      </Card>

      {/* Quick links */}
      <Card>
        <h2 style={{ marginBottom: '1rem' }}>Quick Links</h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          {[
            { href: '/healthcheck', label: '🩺 New Checkup' },
            { href: '/dashboard', label: '📊 Dashboard' },
            { href: '/reports', label: '📄 Reports' },
            { href: '/guidelines', label: '📚 Guidelines' },
          ].map(({ href, label }) => (
            <Link key={href} href={href}>
              <button
                style={{
                  background: '#e6f7ff',
                  color: '#0077b6',
                  border: '1px solid #b3e0f7',
                  borderRadius: '8px',
                  padding: '0.6rem 1.2rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  fontSize: '0.95rem',
                }}
              >
                {label}
              </button>
            </Link>
          ))}
        </div>
      </Card>
    </Layout>
  );
}
