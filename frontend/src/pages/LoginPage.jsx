import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';

export default function LoginPage() {
  const [email, setEmail] = useState('admin@example.com');
  const [password, setPassword] = useState('password123');
  const [mode, setMode] = useState('login');
  const [fullName, setFullName] = useState('Admin User');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (mode === 'register') {
        await api.post('/auth/register', { email, password, full_name: fullName });
      }
      const { data } = await api.post('/auth/login', { email, password });
      login(data.access_token);
      navigate('/');
    } catch (err) {
      setError(err?.response?.data?.detail || 'Authentication failed');
    }
  };

  return (
    <div className="container narrow">
      <h1>Fake News Auth</h1>
      <form onSubmit={submit}>
        {mode === 'register' && <input value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="Full Name" />}
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" type="email" />
        <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" />
        {error && <p className="error">{error}</p>}
        <button type="submit">{mode === 'login' ? 'Sign In' : 'Create Account'}</button>
      </form>
      <button className="link" onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
        Switch to {mode === 'login' ? 'register' : 'login'}
      </button>
    </div>
  );
}
