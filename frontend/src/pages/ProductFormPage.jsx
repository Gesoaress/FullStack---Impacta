import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createProduct, getProduct, updateProduct } from '../services/api';

export default function ProductFormPage() {
  const navigate = useNavigate();
  const { id }   = useParams();
  const isEdit   = Boolean(id);

  const [form, setForm]       = useState({ nome:'', preco:'', quantidade:'', status:'Ativo', img:'' });
  const [error, setError]     = useState('');
  const [loading, setLoading] = useState(false);
  const [fetch_,  setFetch]   = useState(isEdit);

  useEffect(() => {
    if (!isEdit) return;
    (async () => {
      try {
        const d = await getProduct(id);
        setForm({ nome: d.nome??'', preco: d.preco??'', quantidade: d.quantidade??'', status: d.status??'Ativo', img: d.img??'' });
      } catch(e) { setError(e.message); }
      finally { setFetch(false); }
    })();
  }, [id, isEdit]);

  const handle = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }));

  const validate = () => {
    if (!form.nome.trim()) return 'Informe o nome.';
    if (isNaN(parseFloat(form.preco)) || parseFloat(form.preco) < 0) return 'Preço inválido.';
    if (isNaN(parseInt(form.quantidade)) || parseInt(form.quantidade) < 0) return 'Quantidade inválida.';
    return null;
  };

  const submit = async () => {
    const err = validate(); if (err) { setError(err); return; }
    setError(''); setLoading(true);
    const payload = { nome: form.nome.trim(), preco: parseFloat(form.preco), quantidade: parseInt(form.quantidade), status: form.status, img: form.img.trim() };
    try {
      isEdit ? await updateProduct(id, payload) : await createProduct(payload);
      navigate('/produtos');
    } catch(e) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (fetch_) return (
    <div style={{ display:'flex',flexDirection:'column',height:'100%' }}>
      <div className="toolbar"><span className="toolbar-title">{isEdit?'Editar':'Novo'} Produto</span></div>
      <div className="page-content"><div className="empty"><span className="spinner" /></div></div>
    </div>
  );

  const imgOk = form.img.startsWith('http');
  const code  = isEdit ? String(id).padStart(5,'0') : (Math.floor(Math.random()*99999)).toString().padStart(5,'0');

  return (
    <div style={{ display:'flex', flexDirection:'column', height:'100%' }}>
      <div className="toolbar">
        <div style={{ display:'flex', alignItems:'center', gap:8 }}>
          <button className="btn btn-sm btn-sec" onClick={() => navigate('/produtos')}>← Voltar</button>
          <span className="toolbar-title">{isEdit ? 'Editar Produto' : 'Novo Produto'}</span>
        </div>
      </div>

      <div className="page-content">
        <div className="groupbox" style={{ maxWidth:520 }}>
          <div className="groupbox-title">
            {isEdit ? `Editando produto #${code}` : 'Cadastrar novo produto'}
          </div>
          <div className="groupbox-body">
            <div className="form-grid" style={{ gap:10 }}>

              <div className="field" style={{ gridColumn:'1/2' }}>
                <label>Código</label>
                <input value={code} readOnly style={{ background:'#f0f7ea', color:'#777', fontFamily:'monospace' }} />
              </div>

              <div className="field" style={{ gridColumn:'2/3' }}>
                <label>Status</label>
                <select name="status" value={form.status} onChange={handle}>
                  <option value="Ativo">Ativo</option>
                  <option value="Inativo">Inativo</option>
                </select>
              </div>

              <div className="field span-2">
                <label>Nome do Produto</label>
                <input name="nome" placeholder="Digite o nome do produto" value={form.nome} onChange={handle} />
              </div>

              <div className="field">
                <label>Preço</label>
                <input name="preco" type="number" min="0" step="0.01" placeholder="R$ 0,00" value={form.preco} onChange={handle} />
              </div>

              <div className="field">
                <label>Estoque Inicial</label>
                <input name="quantidade" type="number" min="0" placeholder="0" value={form.quantidade} onChange={handle} />
              </div>

              <div className="field span-2">
                <label>Imagem (URL)</label>
                <div className="img-preview-row">
                  <div className="img-box">
                    {imgOk ? <img src={form.img} alt="preview" onError={e=>e.target.style.display='none'} /> : '📦'}
                  </div>
                  <input name="img" placeholder="https://..." value={form.img} onChange={handle} style={{ flex:1 }} />
                </div>
              </div>

              <div className="field span-2">
                <label>Descrição (opcional)</label>
                <textarea name="descricao" placeholder="Digite a descrição do produto..." rows={3} />
              </div>

            </div>

            {error && <div className="err-msg" style={{ marginTop:8 }}>⚠ {error}</div>}

            <div className="form-footer">
              <button className="btn btn-sec" onClick={() => navigate('/produtos')}>Cancelar</button>
              <button className="btn" onClick={submit} disabled={loading}>
                {loading ? <span className="spinner" /> : isEdit ? '💾 Salvar Alterações' : '💾 Salvar Produto'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}