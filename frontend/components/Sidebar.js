import Link from 'next/link';
import { useRouter } from 'next/router';
import styles from '../styles/sidebar.module.css';

const mainLinks = [
  { href: '/', label: 'Home', icon: '🏠' },
  { href: '/healthcheck', label: 'Health Checkup', icon: '🩺' },
  { href: '/dashboard', label: 'Dashboard', icon: '📊' },
  { href: '/history', label: 'Checkup History', icon: '📂' },
  { href: '/reports', label: 'Health Reports', icon: '📄' },
  { href: '/guidelines', label: 'Health Guidelines', icon: '📚' },
  { href: '/profile', label: 'My Profile', icon: '👤' },
];

const authLinks = [
  { href: '/login', label: 'Login', icon: '🔐' },
  { href: '/register', label: 'Register', icon: '📝' },
];

export default function Sidebar({ isLoggedIn, onLogout }) {
  const router = useRouter();

  return (
    <nav className={styles.sidebar}>
      <span className={styles.logo}>🏥 Health Checkup</span>

      {isLoggedIn ? (
        <>
          <div className={styles.section}>Main Menu</div>
          {mainLinks.map(({ href, label, icon }) => (
            <Link
              key={href}
              href={href}
              className={
                router.pathname === href
                  ? `${styles.navItem} ${styles.active}`
                  : styles.navItem
              }
            >
              {icon} {label}
            </Link>
          ))}

          <div className={styles.section}>Account</div>
          <button
            onClick={() => {
              if (typeof window !== 'undefined') {
                localStorage.removeItem('user_id');
                localStorage.removeItem('username');
              }
              if (onLogout) onLogout();
            }}
            className={styles.navItem}
            style={{
              width: '100%',
              textAlign: 'left',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              font: 'inherit',
              borderLeft: '3px solid transparent',
              color: '#dc2626',
            }}
          >
            🚪 Logout
          </button>
        </>
      ) : (
        <>
          <div className={styles.section}>Account</div>
          {authLinks.map(({ href, label, icon }) => (
            <Link
              key={href}
              href={href}
              className={
                router.pathname === href
                  ? `${styles.navItem} ${styles.active}`
                  : styles.navItem
              }
            >
              {icon} {label}
            </Link>
          ))}
        </>
      )}
    </nav>
  );
}
