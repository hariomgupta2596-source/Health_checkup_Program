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
  flex: '1 1 200px',
});
const metricLabel = { fontSize: '0.75rem', color: '#555', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.3rem' };
const metricValue = { fontSize: '1.5rem', fontWeight: '700', color: '#0077b6' };
const recBox = { background: '#f0fdf4', borderLeft: '4px solid #22c55e', borderRadius: '8px', padding: '0.75rem 1rem', marginBottom: '0.5rem', color: '#1a3a52', fontSize: '0.95rem' };

const INITIAL_FORM = {
  name: '',
  age: 30,
  gender: 'Male',
  height_cm: 170,
  weight_kg: 70,
  systolic: 120,
  diastolic: 80,
  heart_rate: 72,
  temperature: 37.0,
  sleep_hours: 7,
  exercise_days: 3,
  water_intake: 8,
  smoking: 'Never',
  alcohol: 'Never',
  stress_level: 'Low',
  other_conditions: '',
  allergies: '',
  medications: '',
  family_history: '',
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
      [name]: type === 'checkbox' ? checked : type === 'number' ? (value === '' ? '' : Number(value)) : value,
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.name.trim()) { setError('Please enter your full name or preferred display name.'); return; }
    setError('');
    setLoading(true);
    try {
      const payload = {
        ...form,
        blood_pressure: `${form.systolic}/${form.diastolic} mmHg`,
      };
      const res = await api.post('/api/checkup', payload);
      setResult(res.data);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit checkup. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Layout>
      <h1 style={{ marginBottom: '0.5rem' }}>🩺 Comprehensive Health Assessment</h1>
      <p style={{ color: '#64748b', marginBottom: '1.5rem' }}>
        Record your vitals, lifestyle habits, and medical history. All metrics are evaluated against standard general wellness reference ranges.
      </p>

      {result && (
        <Card>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2 style={{ color: '#0077b6', margin: 0 }}>📊 Assessment Results & Analysis</h2>
            <button
              onClick={() => router.push('/dashboard')}
              className="btn-primary"
              style={{ fontSize: '0.85rem', padding: '0.4rem 0.8rem' }}
            >
              View in Dashboard →
            </button>
          </div>

          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
            <div style={metricBox('#dff5ff')}>
              <div style={metricLabel}>Body Mass Index</div>
              <div style={metricValue}>{result.bmi}</div>
              <div style={{ fontSize: '0.85rem', fontWeight: 600, color: result.bmi_eval?.color || '#0077b6' }}>
                {result.bmi_eval?.category || 'Calculated'}
              </div>
            </div>

            <div style={metricBox('#eef2ff')}>
              <div style={metricLabel}>Blood Pressure</div>
              <div style={metricValue}>{form.systolic}/{form.diastolic}</div>
              <div style={{ fontSize: '0.85rem', fontWeight: 600, color: result.bp_eval?.color || '#0077b6' }}>
                {result.bp_eval?.category || 'Recorded'}
              </div>
            </div>

            <div style={metricBox('#f0fdf4')}>
              <div style={metricLabel}>Resting Heart Rate</div>
              <div style={metricValue}>{form.heart_rate} bpm</div>
              <div style={{ fontSize: '0.85rem', fontWeight: 600, color: result.hr_eval?.color || '#22c55e' }}>
                {result.hr_eval?.status || 'Recorded'}
              </div>
            </div>

            <div style={metricBox('#fef3c7')}>
              <div style={metricLabel}>Body Temperature</div>
              <div style={metricValue}>{form.temperature} °C</div>
              <div style={{ fontSize: '0.85rem', fontWeight: 600, color: result.temp_eval?.color || '#eab308' }}>
                {result.temp_eval?.status || 'Normal'}
              </div>
            </div>
          </div>

          {result.bmi_eval?.is_pediatric && (
            <div style={{ background: '#e0f2fe', padding: '0.75rem 1rem', borderRadius: '8px', marginBottom: '1rem', color: '#0369a1', fontSize: '0.9rem' }}>
              ℹ️ <strong>Pediatric Note:</strong> {result.bmi_eval.note}
            </div>
          )}

          <h3 style={{ fontSize: '1rem', marginBottom: '0.75rem', color: '#1e293b' }}>💡 Educational Wellness Recommendations</h3>
          {result.recommendations && result.recommendations.map((rec, i) => (
            <div key={i} style={recBox}>
              {rec}
            </div>
          ))}

          <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '1rem', fontStyle: 'italic' }}>
            Disclaimer: {result.disclaimer}
          </p>
        </Card>
      )}

      {error && (
        <div style={{ background: '#fef2f2', border: '1px solid #f87171', color: '#b91c1c', padding: '0.75rem 1rem', borderRadius: '8px', marginBottom: '1.25rem' }}>
          {error}
        </div>
      )}

      <Card>
        <form onSubmit={handleSubmit}>
          {/* Section 1: Personal Info */}
          <div style={sectionTitle}>1. Personal Information</div>
          <div style={gridThree}>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Full Name / Preferred Name *
              </label>
              <input
                type="text"
                name="name"
                placeholder="e.g. Jane Doe"
                value={form.name}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Age (years) *
              </label>
              <input
                type="number"
                name="age"
                min="1"
                max="120"
                value={form.age}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Gender
              </label>
              <select name="gender" value={form.gender} onChange={handleChange}>
                <option>Male</option>
                <option>Female</option>
                <option>Non-binary</option>
                <option>Prefer not to say</option>
              </select>
            </div>
          </div>

          <div style={divider} />

          {/* Section 2: Physical Measurements */}
          <div style={sectionTitle}>2. Physical Measurements</div>
          <div style={gridTwo}>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Height (cm) *
              </label>
              <input
                type="number"
                name="height_cm"
                min="50"
                max="260"
                step="0.5"
                value={form.height_cm}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Weight (kg) *
              </label>
              <input
                type="number"
                name="weight_kg"
                min="2"
                max="300"
                step="0.5"
                value={form.weight_kg}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div style={divider} />

          {/* Section 3: Vital Signs */}
          <div style={sectionTitle}>3. Vital Signs</div>
          <div style={gridThree}>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Systolic BP (mmHg) *
              </label>
              <input
                type="number"
                name="systolic"
                min="60"
                max="250"
                placeholder="120"
                value={form.systolic}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Diastolic BP (mmHg) *
              </label>
              <input
                type="number"
                name="diastolic"
                min="40"
                max="150"
                placeholder="80"
                value={form.diastolic}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Resting Heart Rate (bpm) *
              </label>
              <input
                type="number"
                name="heart_rate"
                min="30"
                max="220"
                value={form.heart_rate}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div style={{ marginTop: '0.75rem' }}>
            <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
              Body Temperature (°C) *
            </label>
            <input
              type="number"
              name="temperature"
              min="34.0"
              max="43.0"
              step="0.1"
              value={form.temperature}
              onChange={handleChange}
              required
            />
          </div>

          <div style={divider} />

          {/* Section 4: Lifestyle Habits */}
          <div style={sectionTitle}>4. Daily Lifestyle Habits</div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ fontSize: '0.85rem', color: '#555', display: 'flex', justifyContent: 'space-between' }}>
              <span>Average Sleep Duration (hours/night):</span>
              <strong style={{ color: '#0077b6' }}>{form.sleep_hours} hrs</strong>
            </label>
            <input
              type="range"
              name="sleep_hours"
              min="0"
              max="14"
              value={form.sleep_hours}
              onChange={handleChange}
              style={{ width: '100%', accentColor: '#0077b6' }}
            />
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ fontSize: '0.85rem', color: '#555', display: 'flex', justifyContent: 'space-between' }}>
              <span>Physical Activity Frequency (days/week):</span>
              <strong style={{ color: '#0077b6' }}>{form.exercise_days} days</strong>
            </label>
            <input
              type="range"
              name="exercise_days"
              min="0"
              max="7"
              value={form.exercise_days}
              onChange={handleChange}
              style={{ width: '100%', accentColor: '#0077b6' }}
            />
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ fontSize: '0.85rem', color: '#555', display: 'flex', justifyContent: 'space-between' }}>
              <span>Daily Water Intake (glasses/day):</span>
              <strong style={{ color: '#0077b6' }}>{form.water_intake} glasses</strong>
            </label>
            <input
              type="range"
              name="water_intake"
              min="0"
              max="20"
              value={form.water_intake}
              onChange={handleChange}
              style={{ width: '100%', accentColor: '#0077b6' }}
            />
          </div>

          <div style={gridThree}>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Smoking Status
              </label>
              <select name="smoking" value={form.smoking} onChange={handleChange}>
                <option>Never</option>
                <option>Former</option>
                <option>Current</option>
              </select>
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Alcohol Consumption
              </label>
              <select name="alcohol" value={form.alcohol} onChange={handleChange}>
                <option>Never</option>
                <option>Rarely</option>
                <option>Occasionally</option>
                <option>Regularly</option>
              </select>
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Perceived Stress Level
              </label>
              <select name="stress_level" value={form.stress_level} onChange={handleChange}>
                <option>Low</option>
                <option>Moderate</option>
                <option>High</option>
                <option>Very High</option>
              </select>
            </div>
          </div>

          <div style={divider} />

          {/* Section 5: Medical History */}
          <div style={sectionTitle}>5. Medical History & Documented Conditions</div>
          <p style={{ fontSize: '0.85rem', color: '#64748b', marginBottom: '0.75rem' }}>
            Check any ongoing conditions that have been diagnosed by a physician:
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.75rem', marginBottom: '1.25rem' }}>
            {[
              { name: 'diabetes', label: 'Diabetes' },
              { name: 'hypertension', label: 'Hypertension' },
              { name: 'asthma', label: 'Asthma' },
              { name: 'heart_disease', label: 'Heart Disease' },
              { name: 'thyroid', label: 'Thyroid Disorder' },
            ].map(({ name, label }) => (
              <label key={name} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', background: '#f8fafc', padding: '0.6rem 0.8rem', borderRadius: '8px' }}>
                <input
                  type="checkbox"
                  name={name}
                  checked={form[name]}
                  onChange={handleChange}
                  style={{ width: 'auto', margin: 0 }}
                />
                <span style={{ fontSize: '0.9rem', color: '#334155' }}>{label}</span>
              </label>
            ))}
          </div>

          <div style={gridTwo}>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Known Allergies (Optional)
              </label>
              <input
                type="text"
                name="allergies"
                placeholder="e.g. Penicillin, Peanuts, Pollen"
                value={form.allergies}
                onChange={handleChange}
              />
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
                Current Medications (Optional)
              </label>
              <input
                type="text"
                name="medications"
                placeholder="e.g. Multivitamin, Lisinopril 10mg"
                value={form.medications}
                onChange={handleChange}
              />
            </div>
          </div>

          <div>
            <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.3rem' }}>
              Family Medical History (Optional)
            </label>
            <input
              type="text"
              name="family_history"
              placeholder="e.g. Family history of heart disease, diabetes"
              value={form.family_history}
              onChange={handleChange}
            />
          </div>

          <div style={{ marginTop: '1.5rem' }}>
            <button
              type="submit"
              className="btn-primary"
              style={{ width: '100%', padding: '0.9rem' }}
              disabled={loading}
            >
              {loading ? 'Analyzing & Saving Assessment…' : '✅ Submit & Save Health Assessment'}
            </button>
          </div>
        </form>
      </Card>
    </Layout>
  );
}
