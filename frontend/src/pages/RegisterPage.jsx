import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { createSeller, activateSeller } from '../services/api';
import WinWindow from '../components/WinWindow';

export default function RegisterPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0); // 0 = form, 1 = code
  const [celular, setCelular] = useState('');
  const [form, setForm] = useState({ nome:'', cnpj:'', email:'', celular:'', senha:'' });
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handle = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }));

  const submitReg = async () => {
    if (Object.values(form).some(v => !v.trim())) { setError('Preencha todos os campos.'); return; }
    setError(''); setLoading(true);
    try {
      await createSeller(form);
      setCelular(form.celular);
      setStep(1);
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  };

  const submitAct = async () => {
    if (code.length !== 4) { setError('Digite o código de 4 dígitos.'); return; }
    setError(''); setLoading(true);
    try {
      await activateSeller(celular, code);
      navigate('/login', { state: { activated: true } });
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  };

  return (
    <div className="auth-page">
      <WinWindow title="Cadastro" icon="📝" className="auth-win" style={{ maxWidth: 420 }}>

        <div className="auth-brand-area">
          <div className="auth-brand-icon">🏪</div>
          <div className="auth-brand-name">MiniMkt</div>
          <div className="auth-brand-sub">Cadastro de Mini Mercado</div>
        </div>

        <div className="auth-body">
          {/* Step indicator */}
          <div className="step-bar">
            {['Cadastro', 'Ativação'].map((s, i) => (
              <div key={s} className={`step${i < step ? ' done' : i === step ? ' active' : ''}`}>
                <div className="step-circle">{i < step ? '✓' : i + 1}</div>
                <div className="step-lbl">{s}</div>
              </div>
            ))}
          </div>

          {step === 0 && (
            <>
              <div className="form-grid">
                <div className="field span-2">
                  <label>Nome do mercado</label>
                  <input name="nome" placeholder="Mini Mercado X" value={form.nome} onChange={handle} />
                </div>
                <div className="field span-2">
                  <label>CNPJ</label>
                  <input name="cnpj" placeholder="00.000.000/0001-00" value={form.cnpj} onChange={handle} />
                </div>
                <div className="field span-2">
                  <label>E-mail</label>
                  <input name="email" type="email" placeholder="mercado@email.com" value={form.email} onChange={handle} />
                </div>
                <div className="field span-2">
                  <label>Celular (WhatsApp)</label>
                  <input name="celular" placeholder="+5511999999999" value={form.celular} onChange={handle} />
                </div>
                <div className="field span-2">
                  <label>Senha</label>
                  <input name="senha" type="password" placeholder="••••••" value={form.senha} onChange={handle} />
                </div>
              </div>
              {error && <div className="err-msg">⚠ {error}</div>}
              <button className="btn btn-full" onClick={submitReg} disabled={loading} style={{ marginTop: 4 }}>
                {loading ? <span className="spinner" /> : 'Cadastrar e receber código →'}
              </button>
            </>
          )}

          {step === 1 && (
            <>
              <div style={{
                background: '#e8f4d8', border: '1px solid #a8cc88',
                borderRadius: 4, padding: '10px 12px',
                fontSize: 12, color: '#2d6a1f'
              }}>
                📲 Código enviado para <strong>{celular}</strong> via WhatsApp. Verifique e insira abaixo.
              </div>
              <div className="field">
                <label>Código de ativação (4 dígitos)</label>
                <input
                  type="text" maxLength={4} placeholder="0000"
                  value={code}
                  onChange={e => setCode(e.target.value.replace(/\D/g, ''))}
                  style={{ fontSize: 22, letterSpacing: '0.35em', textAlign: 'center', fontWeight: 700 }}
                />
              </div>
              {error && <div className="err-msg">⚠ {error}</div>}
              <button className="btn btn-full" onClick={submitAct} disabled={loading} style={{ marginTop: 4 }}>
                {loading ? <span className="spinner" /> : 'Ativar conta'}
              </button>
              <button className="auth-link" onClick={() => setStep(0)} style={{ alignSelf: 'center' }}>
                ← Voltar ao cadastro
              </button>
            </>
          )}
        </div>

        <div className="auth-ver">
          Já tem conta?{' '}
          <Link to="/login" className="auth-link">Entrar</Link>
        </div>
      </WinWindow>
    </div>
  );
}