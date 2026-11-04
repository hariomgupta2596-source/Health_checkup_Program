import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import styles from '../styles/auth.module.css';
import api from '../utils/api';

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({ login_identifier: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await api.post('/api/login', form);
      localStorage.setItem('user_id', res.data.user_id);
      localStorage.setItem('username', res.data.username);
      router.push('/');
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Invalid credentials. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.card}>
        <h1 className={styles.title}>Welcome Back 👋</h1>
        <p className={styles.subtitle}>Sign in to your Health Checkup account</p>

        {error && <div className={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <label style={{ fontSize: '0.9rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
            Username or Email
          </label>
          <input
            type="text"
            name="login_identifier"
            placeholder="Enter username or email"
            value={form.login_identifier}
            onChange={handleChange}
            required
          />

          <label style={{ fontSize: '0.9rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
            Password
          </label>
          <input
            type="password"
            name="password"
            placeholder="Enter your password"
            value={form.password}
            onChange={handleChange}
            required
          />

          <button
            type="submit"
            className="btn-primary"
            style={{ width: '100%', marginTop: '0.5rem' }}
            disabled={loading}
          >
            {loading ? 'Signing in…' : 'Sign In'}
          </button>
        </form>

        <div className={styles.link}>
          Don&apos;t have an account?{' '}
          <Link href="/register">Create one</Link>
        </div>
      </div>
    </div>
  );
}
