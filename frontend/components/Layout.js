import Head from 'next/head';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Sidebar from './Sidebar';
import styles from '../styles/layout.module.css';

export default function Layout({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    setIsLoggedIn(!!userId);
  }, [router.pathname]);

  function handleLogout() {
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    setIsLoggedIn(false);
    router.push('/login');
  }

  return (
    <>
      <Head>
        <title>Health Checkup Program</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <div className={styles.container}>
        <Sidebar isLoggedIn={isLoggedIn} onLogout={handleLogout} />
        <main className={styles.main}>{children}</main>
      </div>
    </>
  );
}
