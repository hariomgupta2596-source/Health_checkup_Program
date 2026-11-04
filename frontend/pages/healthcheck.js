import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import Card from '../components/Card';
import api from '../utils/api';

const sectionTitle = { fontSize: '1.1rem', fontWeight: '600', color: '#1a1a2e', marginBottom: '1rem', marginTop: '0.5rem' };
const divider = { borderTop: '1px solid #eaeaea', margin: '1.25rem 0' };
const gridTwo = { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' };
const gridThree = { display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' };

const metricBox = (bg) => ({
  background: bg || '#e6f7ff',
  borderRadius: '10px',
  padding: '1rem 1.25rem',
  textAlign: 'center',
});
const metricLabel = { fontSize: '0.75rem', color: '#555', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.3rem' };
const metricValue = { fontSize: '1.5rem', fontWeight: '700', color: '#0077b6' };
const recBox = { background: '#e6f7ff', borderRadius: '8px', padding: '0.65rem 1rem', marginBottom: '0.5rem', color: '#1a3a52', fontSize: '0.95rem' };

const INITIAL_FORM = {
  name: '',
  age: 30,
  gender: 'Male',
  height_cm: 170,
  weight_kg: 70,
  blood_pressure: '120/80',
  heart_rate: 72,
  temperature: 37.0,
  sleep_hours: 7,
  exercise_days: 3,
  water_intake: 8,
  smoking: 'Never',
  alcohol: 'Never',
  stress_level: 'Low',
  other_conditions: '',
  diabetes: false,
  hypertension: false,
  asthma: false,
  heart_disease: false,
  thyroid: false,
};

export default function HealthCheckPage() {
  const router = useRouter();
  const [form, setForm] = useState(INITIAL_FORM);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    if (!userId) router.push('/login');
  }, [router]);

  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : type === 'number' ? Number(value) : value,
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.name.trim()) { setError('Please enter your full name.'); return; }
    setError('');
    setLoading(true);
    try {
      const payload = { ...form };
      const res = await api.post('/api/checkup', payload);
      setResult(res.data);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit checkup. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  const bmiStatus = (bmi) => {
    if (bmi < 18.5) return 'Underweight';
    if (bmi < 25) return 'Normal';
    if (bmi < 30) return 'Overweight';
    return 'Obese';
  };

  const hrStatus = (hr) => (hr >= 60 && hr <= 100 ? 'Normal' : 'Check with Doctor');
  const tempStatus = (t) => (t >= 36.5 && t <= 37.5 ? 'Normal' : 'Abnormal');

  return (
    <Layout>
      <h1 style={{ marginBottom: '1.5rem' }}>🩺 Health Checkup Form</h1>

      {result && (
        <Card>
          <h2 style={{ marginBottom: '1rem' }}>📊 Your Health Assessment Results</h2>
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
            <div style={metricBox('#dff5ff')}>
              <div style={metricLabel}>BMI</div>
              <div style={metricValue}>{result.bmi}</div>
              <div style={{ fontSize: '0.8rem', color: '#555', marginTop: '0.2rem' }}>{bmiStatus(result.bmi)}</div>
            </div>
            <div style={metricBox('#fce8e8')}>
              <div style={metricLabel}>Heart Rate</div>
              <div style={{ ...metricValue, color: '#c0392b' }}>{form.heart_rate} bpm</div>
              <div style={{ fontSize: '0.8rem', color: '#555', marginTop: '0.2rem' }}>{hrStatus(form.heart_rate)}</div>
            </div>
            <div style={metricBox('#e8f8e8')}>
              <div style={metricLabel}>Temperature</div>
              <div style={{ ...metricValue, color: '#27ae60' }}>{form.temperature}°C</div>
              <div style={{ fontSize: '0.8rem', color: '#555', marginTop: '0.2rem' }}>{tempStatus(form.temperature)}</div>
            </div>
            <div style={metricBox('#fff8e1')}>
              <div style={metricLabel}>Blood Pressure</div>
              <div style={{ ...metricValue, color: '#e67e22' }}>{form.blood_pressure}</div>
              <div style={{ fontSize: '0.8rem', color: '#555', marginTop: '0.2rem' }}>Monitor</div>
            </div>
          </div>

          <h3 style={{ marginBottom: '0.75rem' }}>💡 Personalised Recommendations</h3>
          {result.recommendations.map((rec, i) => (
            <div key={i} style={recBox}>{rec}</div>
          ))}
          <button
            className="btn-primary"
            style={{ marginTop: '1rem' }}
            onClick={() => setResult(null)}
          >
            Submit Another Checkup
          </button>
        </Card>
      )}

      {!result && (
        <Card>
          {error && (
            <div style={{ background: '#fdf0f0', color: '#e74c3c', borderRadius: '8px', padding: '0.6rem 1rem', marginBottom: '1rem' }}>
              {error}
            </div>
          )}
          <form onSubmit={handleSubmit}>
            {/* Personal Info */}
            <div style={sectionTitle}>👤 Personal Information</div>
            <div style={gridTwo}>
              <div>
                <label>Full Name</label>
                <input name="name" placeholder="John Doe" value={form.name} onChange={handleChange} required />
              </div>
              <div>
                <label>Age</label>
                <input type="number" name="age" min={1} max={120} value={form.age} onChange={handleChange} />
              </div>
            </div>
            <div>
              <label>Gender</label>
              <select name="gender" value={form.gender} onChange={handleChange}>
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
              </select>
            </div>

            <div style={divider} />

            {/* Physical Measurements */}
            <div style={sectionTitle}>📏 Physical Measurements</div>
            <div style={gridTwo}>
              <div>
                <label>Height (cm)</label>
                <input type="number" name="height_cm" min={100} max={250} value={form.height_cm} onChange={handleChange} />
              </div>
              <div>
                <label>Weight (kg)</label>
                <input type="number" name="weight_kg" min={20} max={300} value={form.weight_kg} onChange={handleChange} />
              </div>
            </div>
            <div>
              <label>Blood Pressure (e.g. 120/80)</label>
              <input name="blood_pressure" placeholder="120/80" value={form.blood_pressure} onChange={handleChange} />
            </div>

            <div style={divider} />

            {/* Health Metrics */}
            <div style={sectionTitle}>❤️ Health Metrics</div>
            <div style={gridTwo}>
              <div>
                <label>Heart Rate (bpm)</label>
                <input type="number" name="heart_rate" min={30} max={200} value={form.heart_rate} onChange={handleChange} />
              </div>
              <div>
                <label>Body Temperature (°C)</label>
                <input type="number" name="temperature" step="0.1" min={35} max={42} value={form.temperature} onChange={handleChange} />
              </div>
            </div>

            <div style={divider} />

            {/* Lifestyle Habits (sliders) */}
            <div style={sectionTitle}>🌿 Lifestyle Habits</div>
            {[
              { name: 'sleep_hours', label: 'Average Sleep (hours/day)', min: 0, max: 12 },
              { name: 'exercise_days', label: 'Exercise Days (per week)', min: 0, max: 7 },
              { name: 'water_intake', label: 'Water Intake (glasses/day)', min: 0, max: 15 },
            ].map(({ name, label, min, max }) => (
              <div key={name} style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>{label}</span>
                  <strong style={{ color: '#0077b6' }}>{form[name]}</strong>
                </label>
                <input
                  type="range"
                  name={name}
                  min={min}
                  max={max}
                  value={form[name]}
                  onChange={handleChange}
                  style={{ marginBottom: 0, padding: 0, border: 'none' }}
                />
              </div>
            ))}

            <div style={divider} />

            {/* Health Conditions */}
            <div style={sectionTitle}>🏥 Health Conditions</div>
            <div style={gridThree}>
              {[
                { name: 'diabetes', label: 'Diabetes' },
                { name: 'hypertension', label: 'Hypertension' },
                { name: 'asthma', label: 'Asthma' },
                { name: 'heart_disease', label: 'Heart Disease' },
                { name: 'thyroid', label: 'Thyroid' },
              ].map(({ name, label }) => (
                <label key={name} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    name={name}
                    checked={form[name]}
                    onChange={handleChange}
                    style={{ width: 'auto', marginBottom: 0 }}
                  />
                  {label}
                </label>
              ))}
            </div>
            <div style={{ marginTop: '0.75rem' }}>
              <label>Other Conditions</label>
              <input name="other_conditions" placeholder="If any" value={form.other_conditions} onChange={handleChange} />
            </div>

            <div style={divider} />

            {/* Lifestyle Factors */}
            <div style={sectionTitle}>🌱 Lifestyle Factors</div>
            <div style={gridThree}>
              <div>
                <label>Smoking Status</label>
                <select name="smoking" value={form.smoking} onChange={handleChange}>
                  <option>Never</option>
                  <option>Former</option>
                  <option>Current</option>
                </select>
              </div>
              <div>
                <label>Alcohol Consumption</label>
                <select name="alcohol" value={form.alcohol} onChange={handleChange}>
                  <option>Never</option>
                  <option>Rarely</option>
                  <option>Occasionally</option>
                  <option>Regularly</option>
                </select>
              </div>
              <div>
                <label>Stress Level</label>
                <select name="stress_level" value={form.stress_level} onChange={handleChange}>
                  <option>Low</option>
                  <option>Moderate</option>
                  <option>High</option>
                  <option>Very High</option>
                </select>
              </div>
            </div>

            <div style={divider} />

            <button type="submit" className="btn-primary" style={{ width: '100%', fontSize: '1.05rem' }} disabled={loading}>
              {loading ? 'Submitting…' : '✅ Submit Health Checkup'}
            </button>
          </form>
        </Card>
      )}
    </Layout>
  );
}
