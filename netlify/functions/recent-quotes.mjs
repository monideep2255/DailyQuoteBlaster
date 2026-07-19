// Netlify Function: recent-quotes
// Returns the most recently sent quotes from Neon. Mapped to /api/quotes/recent.
// The frontend expects a JSON array of { text, author, date, category }.
// If the database is empty or unreachable, it returns a small sample so the page
// still renders (the frontend also has its own fallback).

import { neon } from '@neondatabase/serverless';

export const config = { path: '/api/quotes/recent' };

const SAMPLE = [
  { text: 'The best way to predict the future is to create it.', author: 'Abraham Lincoln', date: '2026-07-17', category: 'motivational' },
  { text: 'Whatever anybody says or does, assume positive intent.', author: 'Indra Nooyi', date: '2026-07-16', category: 'wisdom' },
];

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export default async () => {
  const dbUrl = process.env.DATABASE_URL;
  if (!dbUrl) return json(SAMPLE);

  try {
    const sql = neon(dbUrl);
    const rows = await sql`
      SELECT quote_text, quote_author, category, sent_at
      FROM quotes_sent
      ORDER BY sent_at DESC
      LIMIT 12`;

    if (!rows.length) return json(SAMPLE);

    const quotes = rows.map((r) => ({
      text: r.quote_text,
      author: r.quote_author,
      category: r.category,
      date: r.sent_at ? new Date(r.sent_at).toISOString().slice(0, 10) : null,
    }));
    return json(quotes);
  } catch (err) {
    console.error('recent-quotes failed:', err.message);
    return json(SAMPLE);
  }
};
