export function ConfirmDialog({ title, body, confirmLabel, danger, onConfirm, onCancel }) {
  return (
    <dialog open>
      <h2>{title}</h2>
      <p>{body}</p>
      <button onClick={onCancel}>Отмена</button>
      <button className={danger ? 'btn-danger' : 'btn-primary'} onClick={onConfirm}>{confirmLabel}</button>
    </dialog>
  );
}
