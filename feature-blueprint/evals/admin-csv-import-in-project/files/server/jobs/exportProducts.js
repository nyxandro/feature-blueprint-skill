import ExcelJS from 'exceljs';
import { registerWorker } from './queue.js';
import { notifyUser } from '../notifications.js';
import { db } from '../db/index.js';
// Экспорт каталога в xlsx: файл кладётся в хранилище, пользователь получает уведомление со ссылкой.
registerWorker('export-products', async (job) => {
  const { rows } = await db.query('SELECT sku, name, price_kopecks, stock FROM products ORDER BY sku');
  const wb = new ExcelJS.Workbook();
  const ws = wb.addWorksheet('Товары');
  ws.addRows(rows.map((r) => [r.sku, r.name, r.price_kopecks / 100, r.stock]));
  const url = await job.data.storage.save(await wb.xlsx.writeBuffer());
  await notifyUser(job.data.userId, { title: 'Экспорт готов', body: `${rows.length} товаров`, link: url });
});
