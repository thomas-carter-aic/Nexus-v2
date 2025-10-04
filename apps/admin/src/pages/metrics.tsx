import { useQuery } from 'react-query';
import Link from 'next/link';
import styles from '../styles/Home.module.css';

const fetchMetrics = async () => {
const res = await fetch(process.env.NEXT_PUBLIC_PROMETHEUS_URL + '/api/v1/query?query=up');
return res.json();
};

export default function MetricsDashboard() {
const { data, error, isLoading } = useQuery('metrics', fetchMetrics);

return (

Metrics Dashboard
<link href="/">Home | <link href="/client">Client | <link href="/traces">Traces | <link href="/logs">Logs
Prometheus Metrics
{isLoading &&
Loading...

} {error &&
Error: {error.message}

} {data &&
{JSON.stringify(data, null, 2)}
} <iframe src={process.env.NEXT_PUBLIC_GRAFANA_URL} width="100%" height="600px" />
); }
