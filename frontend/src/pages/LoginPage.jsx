import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { login } from '../services/api';
import WinWindow from '../components/WinWindow';

export default function LoginPage() {
  const navigate = useNavigate();
  const { signIn } = useAuth();
  const [form, setForm]     = useState({ email: '', senha: '' });
  const [error, setError]   = useState('');
  const [loading, setLoading] = useState(false);
  const [remember, setRemember] = useState(false);

  const handle = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }));

    const submit = async () => {
    if (!form.email || !form.senha) { setError('Preencha e-mail e senha.'); return; }
    setError(''); setLoading(true);
    try {
      const data = await login(form.email, form.senha);
      signIn(data.token, data.seller);
      navigate('/produtos');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  /*
  const submit = async () => {
    if (!form.email || !form.senha) { setError('Preencha e-mail e senha.'); return; }
    setError(''); setLoading(true);
    try {
      const data = await login(form.email, form.senha);
      signIn(data.token, data.seller);
      navigate('/produtos');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  */
  return (
    <div className="auth-page">
      <WinWindow title="Login" icon="🔐" className="auth-win">

        <div className="auth-brand-area">
          <div className="auth-brand-icon">🏪</div>
          <div className="auth-brand-name">MiniMkt</div>
          <div className="auth-brand-sub">Sistema de Gestão de Estoque</div>
        </div>

        <div className="auth-body">
          <div className="field">
            <label>Usuário</label>
            <input name="email" type="email" placeholder="Digite seu e-mail"
              value={form.email} onChange={handle}
              onKeyDown={e => e.key === 'Enter' && submit()} />
          </div>

          <div className="field">
            <label>Senha</label>
            <input name="senha" type="password" placeholder="Digite sua senha"
              value={form.senha} onChange={handle}
              onKeyDown={e => e.key === 'Enter' && submit()} />
          </div>

          <div className="auth-row">
            <label style={{ display:'flex', alignItems:'center', gap:5, cursor:'pointer', fontSize:11 }}>
              <input type="checkbox" checked={remember} onChange={e => setRemember(e.target.checked)}
                style={{ width:13, height:13 }} />
              Lembrar-me
            </label>
            <button className="auth-link">Esqueceu sua senha?</button>
          </div>

          {error && <div className="err-msg">⚠ {error}</div>}

          <button className="btn btn-full" onClick={submit} disabled={loading}
            style={{ marginTop: 4 }}>
            {loading ? <span className="spinner" /> : 'Entrar'}
          </button>
        </div>

        <div className="auth-ver">
          <Link to="/cadastro" className="auth-link">Cadastrar novo mini mercado</Link>
          {'  ·  '}Versão 1.0.0
        </div>
      </WinWindow>
    </div>
  );
}