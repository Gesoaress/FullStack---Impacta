import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { listProducts, inactivateProduct } from '../services/api';

const fmt  = p => 'R$ ' + Number(p).toFixed(2).replace('.', ',');
const EMOJI = ['📦','🥛','🍚','🫘','🥕','🧀','🍳','🌽','🥜','🧅'];
const em    = n => { let h=0; for(const c of n) h=(h*31+c.charCodeAt(0))&0xffff; return EMOJI[h%EMOJI.length]; };
const PAGE  = 8;

export default function ProductsPage() {
  const navigate = useNavigate();
  const [all,      setAll]      = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [query,    setQuery]    = useState('');
  const [page,     setPage]     = useState(1);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState('');

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try { const d = await listProducts(); setAll(d); setFiltered(d); }
    catch (e) { setError(e.message); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  useEffect(() => {
    const f = all.filter(p => p.nome.toLowerCase().includes(query.toLowerCase()));
    setFiltered(f); setPage(1);
  }, [query, all]);

  const inactivate = async id => {
    if (!window.confirm('Inativar este produto?')) return;
    try { await inactivateProduct(id); await load(); }
    catch (e) { alert(e.message); }
  };

  const stats = { total: all.length, ativo: all.filter(p=>p.status==='Ativo').length, estoque: all.reduce((s,p)=>s+p.quantidade,0), baixo: all.filter(p=>p.quantidade>0&&p.quantidade<15).length };

  const pages = Math.ceil(filtered.length / PAGE);
  const rows  = filtered.slice((page-1)*PAGE, page*PAGE);

  return (
    <div style={{ display:'flex', flexDirection:'column', height:'100%' }}>
      {/* Toolbar */}
      <div className="toolbar">
        <span className="toolbar-title">Produtos</span>
        <div className="toolbar-right">
          <button className="btn btn-sm btn-sec" onClick={load}>↺ Atualizar</button>
          <button className="btn btn-sm" onClick={() => navigate('/produtos/novo')}>+ Novo Produto</button>
          <button className="btn btn-sm btn-sec">⬇ Exportar</button>
        </div>
      </div>

      <div className="page-content" style={{ flex:1, overflowY:'auto' }}>
        {/* Stats */}
        <div className="stats-grid">
          {[
            { icon:'📦', val: stats.total,   lbl:'Total de Produtos', sub:'+12 este mês' },
            { icon:'📊', val: stats.estoque,  lbl:'Estoque Total',     sub:'unidades'     },
            { icon:'📥', val: stats.ativo,    lbl:'Produtos Ativos',   sub:''             },
            { icon:'⚠️', val: stats.baixo,   lbl:'Estoque Baixo',     sub:'precisam reposição' },
          ].map(s => (
            <div className="stat-card" key={s.lbl}>
              <div className="stat-icon">{s.icon}</div>
              <div>
                <div className="stat-val">{s.val}</div>
                <div className="stat-lbl">{s.lbl}</div>
                {s.sub && <div className="stat-sub">{s.sub}</div>}
              </div>
            </div>
          ))}
        </div>

        {error && <div className="err-msg" style={{marginBottom:10}}>⚠ {error}</div>}

        {/* Table */}
        <div className="table-wrap">
          <div className="table-bar">
            <div className="search-box">
              <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="6.5" cy="6.5" r="4"/><path d="M11 11l3 3" strokeLinecap="round"/>
              </svg>
              <input placeholder="Buscar produto..." value={query} onChange={e => setQuery(e.target.value)} />
            </div>
            <select style={{ fontSize:11, padding:'3px 6px', border:'1px solid #7d9070', borderRadius:3, background:'#fff', fontFamily:'var(--font)' }}>
              <option>Categoria: Todos</option>
            </select>
          </div>

          {loading ? (
            <div className="empty"><span className="spinner" /></div>
          ) : rows.length === 0 ? (
            <div className="empty">Nenhum produto encontrado.</div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Produto</th>
                  <th>Categoria</th>
                  <th>Estoque</th>
                  <th>Preço</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((p, i) => {
                  const low = p.quantidade > 0 && p.quantidade < 15;
                  const code = String(p.id).padStart(5, '0');
                  return (
                    <tr key={p.id}>
                      <td style={{ fontFamily:'monospace', fontSize:11, color:'#777' }}>{code}</td>
                      <td>
                        <div style={{ display:'flex', alignItems:'center', gap:6 }}>
                          {p.img
                            ? <img src={p.img} alt="" style={{ width:20,height:20,objectFit:'cover',borderRadius:3 }} />
                            : <span style={{ fontSize:14 }}>{em(p.nome)}</span>}
                          <span style={{ fontWeight:600 }}>{p.nome}</span>
                        </div>
                      </td>
                      <td style={{ color:'#777' }}>{p.categoria ?? 'Geral'}</td>
                      <td style={{ fontWeight:700 }}>{p.quantidade}</td>
                      <td style={{ fontFamily:'monospace', fontWeight:700 }}>{fmt(p.preco)}</td>
                      <td>
                        <span className={`badge ${p.status==='Ativo' ? (low?'badge-low':'badge-ok') : 'badge-off'}`}>
                          {p.status === 'Ativo' ? (low ? '⚠ Baixo' : 'Normal') : 'Inativo'}
                        </span>
                      </td>
                      <td>
                        <div style={{ display:'flex', gap:4 }}>
                          <button className="btn btn-sm btn-sec" onClick={() => navigate(`/produtos/${p.id}/editar`)}
                            title="Editar" style={{ padding:'2px 7px' }}>✏️</button>
                          {p.status === 'Ativo' && (
                            <button className="btn btn-sm btn-danger" onClick={() => inactivate(p.id)}
                              title="Inativar" style={{ padding:'2px 7px' }}>🗑</button>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}

          {/* Pagination */}
          <div className="tbl-footer">
            <span>Mostrando {(page-1)*PAGE+1} a {Math.min(page*PAGE, filtered.length)} de {filtered.length} produtos</span>
            <div className="pg-btns">
              <button className="pg-btn" onClick={() => setPage(p=>Math.max(1,p-1))} disabled={page===1}>‹</button>
              {Array.from({ length: Math.min(pages, 5) }, (_, i) => i+1).map(n => (
                <button key={n} className={`pg-btn${page===n?' active':''}`} onClick={() => setPage(n)}>{n}</button>
              ))}
              {pages > 5 && <span style={{ fontSize:11 }}>…</span>}
              {pages > 5 && <button className="pg-btn" onClick={() => setPage(pages)}>{pages}</button>}
              <button className="pg-btn" onClick={() => setPage(p=>Math.min(pages,p+1))} disabled={page===pages}>›</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}