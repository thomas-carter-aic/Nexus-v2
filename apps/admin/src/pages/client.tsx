import { useQuery, useMutation } from 'react-query';
import Link from 'next/link';
import styles from '../styles/Home.module.css';

const fetchUser = async () => {
const res = await fetch('http://localhost:8000/profile', { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
return res.json();
};

const register = async (user) => {
const res = await fetch('http://localhost:8000/register', { method: 'POST', body: JSON.stringify(user), headers: { 'Content-Type': 'application/json' } });
return res.json();
};

export default function ClientDashboard() {
const { data, error, isLoading } = useQuery('user', fetchUser);
const mutation = useMutation(register);

return (

Client Dashboard
<link href="/register">Register | <link href="/login">Login | <link href="/logout">Logout | <link href="/password/recover">Recover Password | <link href="/password/change">Change Password | <link href="/profile">Profile | <link href="/billing">Billing | <link href="/invoices">Invoices | <link href="/organizations">Organizations | <link href="/teams">Teams | <link href="/projects">Projects | <link href="/tasks">Tasks | <link href="/chat">Chat | <link href="/notifications">Notifications
User Profile
{isLoading &&
Loading...

} {error &&
Error: {error.message}

} {data &&
{JSON.stringify(data, null, 2)}
}
); }
