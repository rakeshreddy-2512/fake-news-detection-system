import { useEffect, useState } from 'react';
import { Pie, PieChart, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import AnalyticsCard from '../components/AnalyticsCard';
import { useAuth } from '../context/AuthContext';
import { api, authHeaders } from '../services/api';

const COLORS = ['#ef4444', '#10b981'];

export default function DashboardPage() {
  const { token, logout } = useAuth();
  const [analytics, setAnalytics] = useState({ total_predictions: 0, fake_count: 0, real_count: 0, fake_ratio: 0, average_confidence: 0 });
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [result, setResult] = useState(null);

  const loadAnalytics = async () => {
    const { data } = await api.get('/analytics', authHeaders(token));
    setAnalytics(data);
  };

  useEffect(() => { loadAnalytics(); }, []);

  const predict = async (e) => {
    e.preventDefault();
    const { data } = await api.post('/predict', { title, content }, authHeaders(token));
    setResult(data);
    setTitle('');
    setContent('');
    loadAnalytics();
  };

  const chartData = [
    { name: 'Fake', value: analytics.fake_count },
    { name: 'Real', value: analytics.real_count },
  ];

  return (
    <div className="container">
      <header><h1>News Classification Dashboard</h1><button onClick={logout}>Logout</button></header>
      <section className="grid">
        <AnalyticsCard title="Total Scans" value={analytics.total_predictions} />
        <AnalyticsCard title="Fake Ratio" value={`${(analytics.fake_ratio * 100).toFixed(1)}%`} />
        <AnalyticsCard title="Avg Confidence" value={`${(analytics.average_confidence * 100).toFixed(1)}%`} />
      </section>

      <section className="chart">
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie data={chartData} dataKey="value" innerRadius={60} outerRadius={100}>
              {chartData.map((entry, idx) => <Cell key={entry.name} fill={COLORS[idx]} />)}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </section>

      <form className="predict" onSubmit={predict}>
        <h2>Classify Article</h2>
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Headline" required />
        <textarea value={content} onChange={(e) => setContent(e.target.value)} placeholder="Article content" rows={6} required />
        <button type="submit">Analyze</button>
      </form>

      {result && <p className="result">Result: <strong>{result.label}</strong> ({(result.confidence * 100).toFixed(2)}%)</p>}
    </div>
  );
}
