import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { listProducts, createSale } from '../services/api';

const fmt  = p => 'R$ ' + Number(p).toFixed(2).replace('.', ',');
const EMOJI = ['📦','🥛','🍚','🫘','🥕','🧀','🍳','🌽','🥜','🧅'];
const em    = n => { let h=0; for(const c of n) h=(h*31+c.charCodeAt(0))&0xffff; return EMOJI[h%EMOJI.length]; };

export default function SalePage() {
  const navigate = useNavigate();
  const [products,   setProducts]   = useState([]);
  const [loading,    setLoading]    = useState(true);
  const [selected,   setSelected]   = useState(null);
  const [qty,        setQty]        = useState(1);
  const [submitting, setSubmitting] = useState(false);
  const [error,      setError]      = useState('');
  const [success,    setSuccess]    = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const d = await listProducts();
      setProducts(d.filter(p => p.status === 'Ativo' && p.quantidade > 0));
    } catch(e) { setError(e.message); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  const select = p => { setSelected(p); setQty(1); setError(''); };

  const dq = d => { if (!selected) return; setQty(q => Math.max(1, Math.min(selected.quantidade, q+d))); };

  const confirm = async () => {
    if (!selected) return;
    if (qty > selected.quantidade) { setError('Estoque insuficiente.'); return; }
    setError(''); setSubmitting(true);
    try {
      await createSale(selected.id, qty);
      setSuccess(true); setSelected(null); setQty(1);
      await load();
      setTimeout(() => setSuccess(false), 3000);
    } catch(e) { setError(e.message); }
    finally { setSubmitting(false); }
  };

  return (
    <div style={{ display:'flex', flexDirection:'column', height:'100%' }}>
      <div className="toolbar">
        <div style={{ display:'flex', alignItems:'center', gap:8 }}>
          <button className="btn btn-sm btn-sec" onClick={() => navigate('/produtos')}>← Voltar</button>
          <span className="toolbar-title">Registrar Venda</span>
        </div>
      </div>

      <div className="page-content">
        {success && (
          <div className="success-bar">
            ✅ Venda registrada com sucesso!
          </div>
        )}

        {loading ? (
          <div className="empty"><span className="spinner" /></div>
        ) : (
          <div className="sale-grid">

            {/* Produto */}
            <div className="groupbox">
              <div className="groupbox-title">Selecionar Produto</div>
              <div style={{ maxHeight:360, overflowY:'auto' }}>
                {products.length === 0 ? (
                  <div className="empty">Nenhum produto ativo em estoque.</div>
                ) : products.map(p => (
                  <div
                    key={p.id}
                    className={`sale-item${selected?.id===p.id?' sel':''}`}
                    onClick={() => select(p)}
                  >
                    <span style={{ fontSize:16 }}>
                      {p.img
                        ? <img src={p.img} alt="" style={{ width:18,height:18,objectFit:'cover',borderRadius:3 }} />
                        : em(p.nome)}
                    </span>
                    <div style={{ flex:1 }}>
                      <div className="sale-item-name">{p.nome}</div>
                      <div className="sale-item-stock">{p.quantidade} em estoque</div>
                    </div>
                    <div className="sale-item-price">{fmt(p.preco)}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Resumo */}
            <div className="groupbox">
              <div className="groupbox-title">Resumo da Venda</div>
              <div className="groupbox-body">
                {!selected ? (
                  <div className="empty" style={{ padding:40 }}>← Selecione um produto</div>
                ) : (
                  <>
                    <div style={{ fontWeight:700, fontSize:13, marginBottom:12 }}>{selected.nome}</div>

                    <div className="summ-row">
                      <span className="summ-k">Preço unitário</span>
                      <span className="summ-v">{fmt(selected.preco)}</span>
                    </div>
                    <div className="summ-row">
                      <span className="summ-k">Disponível</span>
                      <span className="summ-v">{selected.quantidade} un.</span>
                    </div>
                    <div className="summ-row">
                      <span className="summ-k">Quantidade</span>
                      <div className="qty-row">
                        <button className="qty-btn" onClick={() => dq(-1)}>−</button>
                        <span className="qty-num">{qty}</span>
                        <button className="qty-btn" onClick={() => dq(1)}>+</button>
                      </div>
                    </div>

                    <div className="summ-total-row">
                      <span className="summ-total-lbl">Total</span>
                      <span className="summ-total-val">{fmt(selected.preco * qty)}</span>
                    </div>

                    {error && <div className="err-msg" style={{ marginTop:8 }}>⚠ {error}</div>}

                    <button
                      className="btn btn-full"
                      style={{ marginTop:14 }}
                      onClick={confirm}
                      disabled={submitting}
                    >
                      {submitting ? <span className="spinner" /> : '🛒 Confirmar Venda'}
                    </button>

                    <button className="btn btn-sec btn-full" style={{ marginTop:6 }} onClick={() => setSelected(null)}>
                      Cancelar
                    </button>
                  </>
                )}
              </div>
            </div>

          </div>
        )}
      </div>
    </div>
  );
}