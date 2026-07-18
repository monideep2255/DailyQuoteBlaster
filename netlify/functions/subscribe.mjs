// Netlify Function: subscribe
// Inserts a new subscriber into Neon Postgres. Mapped to /api/subscribe via the
// config below (Netlify Functions 2.0 custom path), so the existing frontend
// fetch('/api/subscribe') works unchanged.
//
// Security: DATABASE_URL is a server-side env var, never shipped to the browser.
// All values go into a parameterized query (tagged template), so user input is
// never concatenated into SQL.

import { neon } from '@neondatabase/serverless';

export const config = { path: '/api/subscribe' };

const VALID_CATEGORIES = ['general', 'motivational', 'wisdom', 'growth', 'decisions', 'success'];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export default async (req) => {
  if (req.method !== 'POST') {
    return json({ success: false, message: 'Method not allowed' }, 405);
  }

  const dbUrl = process.env.DATABASE_URL;
  if (!dbUrl) {
    return json({ success: false, message: 'Server not configured' }, 500);
  }

  let data;
  try {
    data = await req.json();
  } catch {
    return json({ success: false, message: 'Invalid request body' }, 400);
  }

  const email = (data.email || '').trim();
  const phone = (data.phone || '').trim();
  const morning = Boolean(data.deliveryTimes ? data.deliveryTimes.morning : data.morning);
  const evening = Boolean(data.deliveryTimes ? data.deliveryTimes.evening : data.evening);

  if (!email && !phone) {
    return json({ success: false, message: 'Provide either an email or a phone number.' }, 400);
  }
  if (email && !EMAIL_RE.test(email)) {
    return json({ success: false, message: 'That email address looks invalid.' }, 400);
  }
  if (!morning && !evening) {
    return json({ success: false, message: 'Select at least one delivery time.' }, 400);
  }

  // Keep only known categories; default to all if none chosen.
  let categories = Array.isArray(data.categories) ? data.categories.filter((c) => VALID_CATEGORIES.includes(c)) : [];
  if (categories.length === 0) categories = VALID_CATEGORIES;

  try {
    const sql = neon(dbUrl);
    // Ensure the table exists (matches database.py schema) so a fresh Neon DB works.
    await sql`
      CREATE TABLE IF NOT EXISTS subscribers (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255),
        phone VARCHAR(50),
        morning_delivery BOOLEAN DEFAULT TRUE,
        evening_delivery BOOLEAN DEFAULT TRUE,
        categories TEXT[],
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        active BOOLEAN DEFAULT TRUE,
        CONSTRAINT email_or_phone CHECK (email IS NOT NULL OR phone IS NOT NULL)
      )`;

    const rows = await sql`
      INSERT INTO subscribers (email, phone, morning_delivery, evening_delivery, categories)
      VALUES (${email || null}, ${phone || null}, ${morning}, ${evening}, ${categories})
      RETURNING id`;

    return json({ success: true, message: 'Subscription successful! You will receive your first quote soon.', id: rows[0].id });
  } catch (err) {
    // Log the error type, never the connection string.
    console.error('subscribe failed:', err.message);
    return json({ success: false, message: 'Subscription failed. Please try again later.' }, 500);
  }
};
