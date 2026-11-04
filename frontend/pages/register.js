import { useState } from 'react';
import Link from 'next/link';
import styles from '../styles/auth.module.css';
import api from '../utils/api';

export default function RegisterPage() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    confirm_password: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (form.password !== form.confirm_password) {
      setError('Passwords do not match.');
      return;
    }
    if (form.password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    setLoading(true);
    try {
      await api.post('/api/register', {
        username: form.username,
        email: form.email,
        password: form.password,
      });
      setSuccess('Registration successful! You can now log in.');
      setForm({ username: '', email: '', password: '', confirm_password: '' });
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Try a different username or email.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.card}>
        <h1 className={styles.title}>Create Account 🏥</h1>
        <p className={styles.subtitle}>Join the Health Checkup Program</p>

        {error && <div className={styles.error}>{error}</div>}
        {success && (
          <div className={styles.success}>
            {success}{' '}
            <Link href="/login" style={{ color: '#0077b6', fontWeight: 600 }}>
              Login now →
            </Link>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <label style={{ fontSize: '0.9rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
            Username
          </label>
          <input
            type="text"
            name="username"
            placeholder="Choose a username"
            value={form.username}
            onChange={handleChange}
            required
          />

          <label style={{ fontSize: '0.9rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
            Email
          </label>
          <input
            type="email"
            name="email"
            placeholder="your@email.com"
            value={form.email}
            onChange={handleChange}
            required
          />

          <label style={{ fontSize: '0.9rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
            Password
          </label>
          <input
            type="password"
            name="password"
            placeholder="At least 6 characters"
            value={form.password}
            onChange={handleChange}
            required
          />

          <label style={{ fontSize: '0.9rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
            Confirm Password
          </label>
          <input
            type="password"
            name="confirm_password"
            placeholder="Repeat your password"
            value={form.confirm_password}
            onChange={handleChange}
            required
          />

          <button
            type="submit"
            className="btn-primary"
            style={{ width: '100%', marginTop: '0.5rem' }}
            disabled={loading}
          >
            {loading ? 'Creating account…' : 'Create Account'}
          </button>
        </form>

        <div className={styles.link}>
          Already have an account?{' '}
          <Link href="/login">Sign in</Link>
        </div>
      </div>
    </div>
  );
}
