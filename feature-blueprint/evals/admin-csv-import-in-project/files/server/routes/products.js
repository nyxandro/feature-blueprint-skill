import { Router } from 'express';
import { db } from '../db/index.js';
import { AppError } from '../errors.js';
import { jobsQueue } from '../jobs/queue.js';
export const products = Router();
products.get('/', async (req, res) => {
  const page = Number(req.query.page ?? 1);
  const { rows } = await db.query('SELECT * FROM products ORDER BY updated_at DESC LIMIT 50 OFFSET $1', [(page - 1) * 50]);
  res.json({ items: rows, page });
});
products.post('/', async (req, res) => {
  const { sku, name, price_kopecks, stock, category_id } = req.body;
  try {
    const { rows } = await db.query('INSERT INTO products (sku,name,price_kopecks,stock,category_id) VALUES ($1,$2,$3,$4,$5) RETURNING *', [sku, name, price_kopecks, stock, category_id]);
    res.status(201).json(rows[0]);
  } catch (e) {
    if (e.code === '23505') throw new AppError('APP_PRODUCT_SKU_TAKEN', 'Товар с таким артикулом уже есть', 'Проверьте артикул или откройте существующий товар', { cause: e });
    throw e;
  }
});
products.post('/export', async (req, res) => {
  await jobsQueue.add('export-products', { userId: req.user.id });
  res.status(202).json({ queued: true });
});
