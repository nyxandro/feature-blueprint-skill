import { useState, useEffect } from 'react';
import { Toast } from '../components/Toast.jsx';
import { AddProductModal } from '../components/AddProductModal.jsx';
export function ProductsPage() {
  const [items, setItems] = useState([]);
  const [adding, setAdding] = useState(false);
  const [toast, setToast] = useState(null);
  useEffect(() => { fetch('/api/products').then((r) => r.json()).then((d) => setItems(d.items)); }, []);
  async function exportAll() {
    await fetch('/api/products/export', { method: 'POST' });
    setToast({ kind: 'success', title: 'Экспорт запущен', text: 'Пришлём уведомление, когда файл будет готов' });
  }
  return (
    <section>
      <h1>Товары</h1>
      <button onClick={() => setAdding(true)}>Добавить товар</button>
      <button onClick={exportAll}>Выгрузить в Excel</button>
      <table>{/* sku, название, цена, остаток */}</table>
      {adding && <AddProductModal onClose={() => setAdding(false)} />}
      {toast && <Toast {...toast} />}
    </section>
  );
}
