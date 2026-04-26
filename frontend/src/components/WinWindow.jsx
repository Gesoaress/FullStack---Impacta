// Componente de Janela estilo Windows XP
export default function WinWindow({ title, icon = '🪟', children, className = '' }) {
  return (
    <div className={`win ${className}`}>
      <div className="win-title">
        <span className="win-title-icon">{icon}</span>
        <span className="win-title-text">MiniMkt – {title}</span>
        <div className="win-btns">
          <div className="win-btn">─</div>
          <div className="win-btn">□</div>
          <div className="win-btn x">✕</div>
        </div>
      </div>
      {children}
    </div>
  );
}