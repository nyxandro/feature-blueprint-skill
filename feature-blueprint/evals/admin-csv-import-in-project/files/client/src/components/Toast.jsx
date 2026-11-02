// Всплывающее сообщение. Ошибки не исчезают сами; успех — через 5 с.
export function Toast({ kind = 'success', title, text, code, action }) {
  return (
    <div role={kind === 'error' ? 'alert' : 'status'} className={`toast toast-${kind}`}>
      <strong>{title}</strong>
      <p>{text}</p>
      {code && <small>Код: {code}</small>}
      {action && <button onClick={action.onClick}>{action.label}</button>}
    </div>
  );
}
