import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import Card from '../components/Card';
import api from '../utils/api';

export default function ProfilePage() {
  const router = useRouter();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editForm, setEditForm] = useState({ display_name: '', age: '', gender: 'Male' });
  const [pwdForm, setPwdForm] = useState({ current_password: '', new_password: '', confirm_password: '' });
  const [profileMsg, setProfileMsg] = useState({ type: '', text: '' });
  const [pwdMsg, setPwdMsg] = useState({ type: '', text: '' });

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      router.push('/login');
      return;
    }
    loadProfile();
  }, [router]);

  async function loadProfile() {
    setLoading(true);
    try {
      const res = await api.get('/api/profile');
      setProfile(res.data);
      setEditForm({
        display_name: res.data.display_name || '',
        age: res.data.age || '',
        gender: res.data.gender || 'Male',
      });
    } catch (err) {
      setProfileMsg({ type: 'error', text: err.response?.data?.detail || 'Failed to load profile.' });
    } finally {
      setLoading(false);
    }
  }

  async function handleProfileSubmit(e) {
    e.preventDefault();
    setProfileMsg({ type: '', text: '' });
    try {
      const res = await api.put('/api/profile', {
        display_name: editForm.display_name,
        age: editForm.age ? Number(editForm.age) : null,
        gender: editForm.gender,
      });
      setProfileMsg({ type: 'success', text: res.data.message || 'Profile updated successfully!' });
      loadProfile();
    } catch (err) {
      setProfileMsg({ type: 'error', text: err.response?.data?.detail || 'Failed to update profile.' });
    }
  }

  async function handlePasswordSubmit(e) {
    e.preventDefault();
    setPwdMsg({ type: '', text: '' });

    if (pwdForm.new_password !== pwdForm.confirm_password) {
      setPwdMsg({ type: 'error', text: 'New passwords do not match.' });
      return;
    }
    if (pwdForm.new_password.length < 6) {
      setPwdMsg({ type: 'error', text: 'New password must be at least 6 characters.' });
      return;
    }

    try {
      const res = await api.put('/api/profile/password', {
        current_password: pwdForm.current_password,
        new_password: pwdForm.new_password,
      });
      setPwdMsg({ type: 'success', text: res.data.message || 'Password changed successfully!' });
      setPwdForm({ current_password: '', new_password: '', confirm_password: '' });
    } catch (err) {
      setPwdMsg({ type: 'error', text: err.response?.data?.detail || 'Failed to change password.' });
    }
  }

  return (
    <Layout>
      <h1 style={{ marginBottom: '0.5rem' }}>👤 My Profile & Account Settings</h1>
      <p style={{ color: '#64748b', marginBottom: '1.5rem' }}>
        Manage your personal information, update security settings, and review privacy controls.
      </p>

      {loading ? (
        <Card><p style={{ textAlign: 'center', color: '#64748b' }}>Loading profile information…</p></Card>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
          {/* Account Overview */}
          <div>
            <Card>
              <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: '#0077b6' }}>📋 Profile Overview</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.95rem' }}>
                <div><strong>Username:</strong> {profile?.username}</div>
                <div><strong>Email:</strong> {profile?.email}</div>
                <div><strong>Member Since:</strong> {profile?.created_at ? new Date(profile.created_at).toLocaleDateString() : '—'}</div>
                <div style={{
                  background: '#e0f2fe',
                  padding: '0.75rem 1rem',
                  borderRadius: '8px',
                  color: '#0369a1',
                  fontWeight: 600,
                  marginTop: '0.5rem'
                }}>
                  📊 Total Health Assessments Recorded: {profile?.total_checkups || 0}
                </div>
              </div>
            </Card>

            <Card>
              <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: '#1e293b' }}>✏️ Edit Profile Details</h2>
              {profileMsg.text && (
                <div style={{
                  padding: '0.6rem 0.8rem',
                  borderRadius: '6px',
                  fontSize: '0.9rem',
                  marginBottom: '1rem',
                  background: profileMsg.type === 'success' ? '#f0fdf4' : '#fef2f2',
                  color: profileMsg.type === 'success' ? '#15803d' : '#b91c1c',
                }}>
                  {profileMsg.text}
                </div>
              )}
              <form onSubmit={handleProfileSubmit}>
                <div style={{ marginBottom: '0.75rem' }}>
                  <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
                    Display Name
                  </label>
                  <input
                    type="text"
                    value={editForm.display_name}
                    onChange={(e) => setEditForm({ ...editForm, display_name: e.target.value })}
                    placeholder="Preferred display name"
                  />
                </div>
                <div style={{ marginBottom: '0.75rem' }}>
                  <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
                    Default Age
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="120"
                    value={editForm.age}
                    onChange={(e) => setEditForm({ ...editForm, age: e.target.value })}
                    placeholder="Age"
                  />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
                    Gender
                  </label>
                  <select
                    value={editForm.gender}
                    onChange={(e) => setEditForm({ ...editForm, gender: e.target.value })}
                  >
                    <option>Male</option>
                    <option>Female</option>
                    <option>Non-binary</option>
                    <option>Prefer not to say</option>
                  </select>
                </div>
                <button type="submit" className="btn-primary" style={{ width: '100%' }}>
                  Save Profile Changes
                </button>
              </form>
            </Card>
          </div>

          {/* Security & Privacy */}
          <div>
            <Card>
              <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: '#1e293b' }}>🔐 Change Password</h2>
              {pwdMsg.text && (
                <div style={{
                  padding: '0.6rem 0.8rem',
                  borderRadius: '6px',
                  fontSize: '0.9rem',
                  marginBottom: '1rem',
                  background: pwdMsg.type === 'success' ? '#f0fdf4' : '#fef2f2',
                  color: pwdMsg.type === 'success' ? '#15803d' : '#b91c1c',
                }}>
                  {pwdMsg.text}
                </div>
              )}
              <form onSubmit={handlePasswordSubmit}>
                <div style={{ marginBottom: '0.75rem' }}>
                  <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
                    Current Password
                  </label>
                  <input
                    type="password"
                    value={pwdForm.current_password}
                    onChange={(e) => setPwdForm({ ...pwdForm, current_password: e.target.value })}
                    required
                  />
                </div>
                <div style={{ marginBottom: '0.75rem' }}>
                  <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
                    New Password
                  </label>
                  <input
                    type="password"
                    value={pwdForm.new_password}
                    onChange={(e) => setPwdForm({ ...pwdForm, new_password: e.target.value })}
                    required
                  />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ fontSize: '0.85rem', color: '#555', display: 'block', marginBottom: '0.25rem' }}>
                    Confirm New Password
                  </label>
                  <input
                    type="password"
                    value={pwdForm.confirm_password}
                    onChange={(e) => setPwdForm({ ...pwdForm, confirm_password: e.target.value })}
                    required
                  />
                </div>
                <button type="submit" className="btn-primary" style={{ width: '100%' }}>
                  Update Password
                </button>
              </form>
            </Card>

            <Card>
              <h2 style={{ fontSize: '1.25rem', marginBottom: '0.75rem', color: '#0f766e' }}>🛡️ Privacy & Data Protection</h2>
              <p style={{ fontSize: '0.9rem', color: '#334155', lineHeight: 1.6 }}>
                Your privacy and personal health records are strictly protected:
              </p>
              <ul style={{ fontSize: '0.85rem', color: '#475569', lineHeight: 1.6, paddingLeft: '1.25rem' }}>
                <li><strong>Local Secure Storage:</strong> Your records are securely maintained in isolated relational SQLite database tables.</li>
                <li><strong>Strict User Isolation:</strong> You are the only person who can view or download your assessments.</li>
                <li><strong>No Third-Party Transmission:</strong> Your personal vitals and lifestyle habits are never sold, shared, or sent to external AI APIs.</li>
                <li><strong>Educational Purpose:</strong> All assessments are calculated on your private backend for wellness awareness only.</li>
              </ul>
            </Card>
          </div>
        </div>
      )}
    </Layout>
  );
}
