import { useQuery } from 'react-query';
import Link from 'next/link';
import styles from '../styles/Home.module.css';

const fetchHealth = async () => {
  const res = await fetch('http://localhost:8000/health');
  return res.json();
};

export default function AdminDashboard() {
  const { data, error, isLoading } = useQuery('health', fetchHealth);

  return (

    Admin Dashboard
    <link href="/client">Client Dashboard | <link href="/metrics">Metrics | <link href="/traces">Traces | <link href="/logs">Logs
    Auth Service Health
    {isLoading &&
        Loading...
    } {error &&
Error: {error.message}

} {data &&
{JSON.stringify(data, null, 2)}
}
); 
}
