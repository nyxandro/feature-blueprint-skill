import { db } from './db/index.js';
// Уведомление в колокольчике админки; link открывает нужную страницу.
export async function notifyUser(userId, { title, body, link, level = 'info' }) {
  await db.query('INSERT INTO notifications (user_id, title, body, link, level) VALUES ($1,$2,$3,$4,$5)', [userId, title, body, link, level]);
}
