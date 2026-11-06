import { Queue, Worker } from 'bullmq';
const connection = { url: process.env.REDIS_URL };
export const jobsQueue = new Queue('admin-jobs', { connection });
export function registerWorker(name, handler) {
  return new Worker('admin-jobs', async (job) => (job.name === name ? handler(job) : undefined), { connection });
}
