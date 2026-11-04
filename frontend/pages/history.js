import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import Card from '../components/Card';
import api from '../utils/api';

export default function HistoryPage() {
  const router = useRouter();
  const [history, setHistory] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedCheckup, setSelectedCheckup] = useState(null);
  const [deleteConfirmId, setDeleteConfirmId] = useState(null);
  const [compareIds, setCompareIds] = useState([]);

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      router.push('/login');
      return;
    }
    fetchHistory();
  }, [router]);

  async function fetchHistory(query = '') {
    setLoading(true);
    setError('');
    try {
      const url = query ? `/api/history?q=${encodeURIComponent(query)}` : '/api/history';
      const res = await api.get(url);
      setHistory(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load assessment history.');
    } finally {
      setLoading(false);
    }
  }

  function handleSearchSubmit(e) {
    e.preventDefault();
    fetchHistory(search);
  }

  async function handleDelete(id) {
    try {
      await api.delete(`/api/checkup/${id}`);
      setDeleteConfirmId(null);
      if (selectedCheckup?.id === id) setSelectedCheckup(null);
      setCompareIds((prev) => prev.filter((item) => item !== id));
      fetchHistory(search);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to delete assessment.');
    }
  }

  function toggleCompare(id) {
    if (compareIds.includes(id)) {
      setCompareIds(compareIds.filter((item) => item !== id));
    } else {
      if (compareIds.length >= 2) {
        setCompareIds([compareIds[1], id]);
      } else {
        setCompareIds([...compareIds, id]);
      }
    }
  }

  const checkup1 = history.find((c) => c.id === compareIds[0]);
  const checkup2 = history.find((c) => c.id === compareIds[1]);

  return (
    <Layout>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ margin: 0 }}>📂 Assessment History & Comparison</h1>
          <p style={{ color: '#64748b', margin: '0.25rem 0 0 0' }}>
            Review, search, compare, or manage all your past health checkups.
          </p>
        </div>
        <button
          onClick={() => router.push('/healthcheck')}
          className="btn-primary"
          style={{ padding: '0.6rem 1.2rem', fontSize: '0.9rem' }}
        >
          + New Checkup
        </button>
      </div>

      {/* Comparison Drawer if 2 checkups selected */}
      {checkup1 && checkup2 && (
        <Card>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2 style={{ color: '#0077b6', margin: 0 }}>⚖️ Side-by-Side Assessment Comparison</h2>
            <button
              onClick={() => setCompareIds([])}
              style={{ background: 'none', border: '1px solid #cbd5e1', padding: '0.3rem 0.75rem', borderRadius: '6px', cursor: 'pointer' }}
            >
              Clear Comparison
            </button>
          </div>

          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
              <thead>
                <tr style={{ background: '#f1f5f9' }}>
                  <th style={{ padding: '0.75rem', border: '1px solid #e2e8f0' }}>Metric</th>
                  <th style={{ padding: '0.75rem', border: '1px solid #e2e8f0', color: '#0077b6' }}>
                    Earlier: {new Date(checkup1.date).toLocaleDateString()}
                  </th>
                  <th style={{ padding: '0.75rem', border: '1px solid #e2e8f0', color: '#0284c7' }}>
                    Recent: {new Date(checkup2.date).toLocaleDateString()}
                  </th>
                  <th style={{ padding: '0.75rem', border: '1px solid #e2e8f0' }}>Change / Difference</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { label: 'BMI (kg/m²)', v1: checkup1.bmi, v2: checkup2.bmi, unit: '' },
                  { label: 'Weight (kg)', v1: checkup1.weight_kg, v2: checkup2.weight_kg, unit: 'kg' },
                  { label: 'Blood Pressure', v1: checkup1.blood_pressure, v2: checkup2.blood_pressure, unit: '' },
                  { label: 'Heart Rate (bpm)', v1: checkup1.heart_rate, v2: checkup2.heart_rate, unit: 'bpm' },
                  { label: 'Temperature (°C)', v1: checkup1.temperature, v2: checkup2.temperature, unit: '°C' },
                  { label: 'Sleep (hours/day)', v1: checkup1.sleep_hours, v2: checkup2.sleep_hours, unit: 'hrs' },
                  { label: 'Exercise (days/week)', v1: checkup1.exercise_days, v2: checkup2.exercise_days, unit: 'days' },
                  { label: 'Water (glasses/day)', v1: checkup1.water_intake, v2: checkup2.water_intake, unit: 'glasses' },
                ].map(({ label, v1, v2, unit }, idx) => {
                  const numDiff = typeof v1 === 'number' && typeof v2 === 'number' ? (v2 - v1).toFixed(1) : null;
                  return (
                    <tr key={idx} style={{ borderBottom: '1px solid #f1f5f9' }}>
                      <td style={{ padding: '0.6rem 0.75rem', fontWeight: 600, border: '1px solid #e2e8f0' }}>{label}</td>
                      <td style={{ padding: '0.6rem 0.75rem', border: '1px solid #e2e8f0' }}>{v1} {unit}</td>
                      <td style={{ padding: '0.6rem 0.75rem', border: '1px solid #e2e8f0' }}>{v2} {unit}</td>
                      <td style={{ padding: '0.6rem 0.75rem', border: '1px solid #e2e8f0' }}>
                        {numDiff !== null ? (
                          <span style={{ color: Number(numDiff) === 0 ? '#64748b' : Number(numDiff) > 0 ? '#0284c7' : '#22c55e', fontWeight: 600 }}>
                            {Number(numDiff) > 0 ? `+${numDiff}` : numDiff} {unit}
                          </span>
                        ) : '—'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Search and Filters */}
      <Card>
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <input
            type="text"
            placeholder="Search by condition, notes, medications, or date..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ flex: 1, minWidth: '240px', margin: 0 }}
          />
          <button type="submit" className="btn-primary" style={{ padding: '0.6rem 1.2rem' }}>
            🔍 Search
          </button>
          {search && (
            <button
              type="button"
              onClick={() => { setSearch(''); fetchHistory(''); }}
              style={{ padding: '0.6rem 1rem', background: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '8px', cursor: 'pointer' }}
            >
              Reset
            </button>
          )}
        </form>

        <div style={{ marginTop: '0.75rem', fontSize: '0.85rem', color: '#64748b' }}>
          Tip: Check any 2 boxes on the left to activate <strong>Side-by-Side Comparison</strong>.
        </div>
      </Card>

      {/* History Table */}
      <Card>
        {loading ? (
          <p style={{ textAlign: 'center', color: '#64748b', padding: '2rem 0' }}>Loading assessment history…</p>
        ) : error ? (
          <p style={{ color: '#ef4444' }}>{error}</p>
        ) : history.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem 0' }}>
            <p style={{ fontSize: '1.1rem', color: '#64748b' }}>No health checkup assessments recorded yet.</p>
            <button onClick={() => router.push('/healthcheck')} className="btn-primary">
              Take Your First Checkup →
            </button>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #e2e8f0', color: '#475569' }}>
                  <th style={{ padding: '0.75rem', width: '40px' }}>Compare</th>
                  <th style={{ padding: '0.75rem' }}>Date & Time</th>
                  <th style={{ padding: '0.75rem' }}>BMI</th>
                  <th style={{ padding: '0.75rem' }}>Blood Pressure</th>
                  <th style={{ padding: '0.75rem' }}>Heart Rate</th>
                  <th style={{ padding: '0.75rem' }}>Conditions</th>
                  <th style={{ padding: '0.75rem', textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {history.map((chk) => {
                  const isChecked = compareIds.includes(chk.id);
                  return (
                    <tr key={chk.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                      <td style={{ padding: '0.75rem' }}>
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => toggleCompare(chk.id)}
                          style={{ margin: 0, cursor: 'pointer' }}
                          title="Select to compare"
                        />
                      </td>
                      <td style={{ padding: '0.75rem', fontWeight: 600, color: '#1e293b' }}>
                        {new Date(chk.date).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' })}
                      </td>
                      <td style={{ padding: '0.75rem' }}>
                        <span style={{
                          background: chk.bmi >= 25 ? '#ffedd5' : chk.bmi < 18.5 ? '#fef9c3' : '#dcfce7',
                          color: chk.bmi >= 25 ? '#c2410c' : chk.bmi < 18.5 ? '#a16207' : '#15803d',
                          padding: '0.2rem 0.5rem',
                          borderRadius: '6px',
                          fontWeight: 600,
                          fontSize: '0.85rem'
                        }}>
                          {chk.bmi}
                        </span>
                      </td>
                      <td style={{ padding: '0.75rem' }}>{chk.blood_pressure}</td>
                      <td style={{ padding: '0.75rem' }}>{chk.heart_rate} bpm</td>
                      <td style={{ padding: '0.75rem' }}>
                        {chk.conditions && chk.conditions.length > 0 ? (
                          <div style={{ display: 'flex', gap: '0.25rem', flexWrap: 'wrap' }}>
                            {chk.conditions.map((c, i) => (
                              <span key={i} style={{ background: '#f1f5f9', color: '#475569', fontSize: '0.75rem', padding: '0.15rem 0.4rem', borderRadius: '4px' }}>
                                {c}
                              </span>
                            ))}
                          </div>
                        ) : (
                          <span style={{ color: '#94a3b8' }}>None</span>
                        )}
                      </td>
                      <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                        <button
                          onClick={() => setSelectedCheckup(chk)}
                          style={{
                            background: '#e0f2fe',
                            border: 'none',
                            color: '#0284c7',
                            padding: '0.35rem 0.75rem',
                            borderRadius: '6px',
                            cursor: 'pointer',
                            marginRight: '0.5rem',
                            fontWeight: 600,
                            fontSize: '0.8rem',
                          }}
                        >
                          View
                        </button>
                        <button
                          onClick={() => setDeleteConfirmId(chk.id)}
                          style={{
                            background: '#fee2e2',
                            border: 'none',
                            color: '#ef4444',
                            padding: '0.35rem 0.75rem',
                            borderRadius: '6px',
                            cursor: 'pointer',
                            fontWeight: 600,
                            fontSize: '0.8rem',
                          }}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      {/* Delete Confirmation Modal */}
      {deleteConfirmId && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
        }}>
          <div style={{ background: '#fff', borderRadius: '12px', padding: '2rem', maxWidth: '420px', width: '90%', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.2)' }}>
            <h3 style={{ margin: '0 0 0.75rem 0', color: '#b91c1c' }}>Confirm Deletion</h3>
            <p style={{ color: '#475569', fontSize: '0.95rem', marginBottom: '1.5rem' }}>
              Are you sure you want to permanently delete this health assessment record? This action cannot be undone.
            </p>
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
              <button
                onClick={() => setDeleteConfirmId(null)}
                style={{ padding: '0.5rem 1rem', background: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '6px', cursor: 'pointer' }}
              >
                Cancel
              </button>
              <button
                onClick={() => handleDelete(deleteConfirmId)}
                style={{ padding: '0.5rem 1rem', background: '#ef4444', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 600 }}
              >
                Delete Permanently
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Detail Modal */}
      {selectedCheckup && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
        }}>
          <div style={{ background: '#fff', borderRadius: '16px', padding: '2rem', maxWidth: '640px', width: '90%', maxHeight: '85vh', overflowY: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h2 style={{ margin: 0, color: '#0077b6' }}>Assessment Details</h2>
              <button
                onClick={() => setSelectedCheckup(null)}
                style={{ background: 'none', border: 'none', fontSize: '1.25rem', cursor: 'pointer', color: '#64748b' }}
              >
                ✕
              </button>
            </div>

            <p style={{ color: '#64748b', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
              Recorded on {new Date(selectedCheckup.date).toLocaleString()}
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '1.25rem', fontSize: '0.9rem' }}>
              <div><strong>Height:</strong> {selectedCheckup.height_cm} cm</div>
              <div><strong>Weight:</strong> {selectedCheckup.weight_kg} kg</div>
              <div><strong>BMI:</strong> {selectedCheckup.bmi}</div>
              <div><strong>Blood Pressure:</strong> {selectedCheckup.blood_pressure}</div>
              <div><strong>Heart Rate:</strong> {selectedCheckup.heart_rate} bpm</div>
              <div><strong>Body Temperature:</strong> {selectedCheckup.temperature} °C</div>
              <div><strong>Sleep:</strong> {selectedCheckup.sleep_hours} hrs/day</div>
              <div><strong>Exercise:</strong> {selectedCheckup.exercise_days} days/week</div>
              <div><strong>Water Intake:</strong> {selectedCheckup.water_intake} glasses/day</div>
              <div><strong>Smoking:</strong> {selectedCheckup.smoking}</div>
              <div><strong>Alcohol:</strong> {selectedCheckup.alcohol}</div>
              <div><strong>Stress Level:</strong> {selectedCheckup.stress_level}</div>
            </div>

            <div style={{ borderTop: '1px solid #f1f5f9', paddingTop: '1rem', fontSize: '0.9rem' }}>
              <div style={{ marginBottom: '0.5rem' }}>
                <strong>Allergies:</strong> {selectedCheckup.allergies || 'None reported'}
              </div>
              <div style={{ marginBottom: '0.5rem' }}>
                <strong>Current Medications:</strong> {selectedCheckup.medications || 'None reported'}
              </div>
              <div style={{ marginBottom: '0.5rem' }}>
                <strong>Family History:</strong> {selectedCheckup.family_history || 'None reported'}
              </div>
              <div style={{ marginBottom: '0.5rem' }}>
                <strong>Documented Conditions:</strong>{' '}
                {selectedCheckup.conditions && selectedCheckup.conditions.length > 0
                  ? selectedCheckup.conditions.join(', ')
                  : 'None reported'}
              </div>
            </div>

            <div style={{ marginTop: '1.5rem', textAlign: 'right' }}>
              <button
                onClick={() => setSelectedCheckup(null)}
                className="btn-primary"
                style={{ padding: '0.5rem 1.25rem' }}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
}
