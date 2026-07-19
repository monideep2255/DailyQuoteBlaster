# Daily Quote Sender

Live site: https://dailyquoteblaster.netlify.app

A twice-daily inspirational quote sender. It emails a quote to every active subscriber at 7 AM and 9 PM Eastern, picking the category by the day and time, and records each send. The web page lets anyone subscribe and view recently sent quotes.

- Live app: https://dailyquoteblaster.netlify.app
- How to try it as a new user: [docs/test-cases.md](docs/test-cases.md)

*Last updated: July 19, 2026. Migrated off Replit to a fully free serverless stack.*

## Contents

- [What it does](#what-it-does)
- [Architecture](#architecture)
- [How to run it yourself](#how-to-run-it-yourself)
- [Project structure](#project-structure)
- [Local development](#local-development)
- [Testing](#testing)

## What it does

- Picks a quote whose category depends on the weekday and time of day
- At 7 AM and 9 PM Eastern, emails it to every active subscriber
- Records each send in the database so the site can show recent quotes
- Lets visitors subscribe through a form and choose delivery times and categories

Email is the active channel. The SMS code (Twilio) is kept but disabled by leaving its credentials unset, so there is no per-message cost.

## Architecture

The app runs entirely on free tiers with no always-on server.

- Frontend: static HTML, CSS, and JavaScript in `frontend/`, hosted on Netlify.
- APIs: two Netlify Functions in `netlify/functions/`, `subscribe` (mapped to `/api/subscribe`) and `recent-quotes` (mapped to `/api/quotes/recent`). They talk to the database with parameterized queries over a server-side `DATABASE_URL`.
- Database: Neon serverless Postgres. Two tables, `subscribers` and `quotes_sent`, auto-create on first use.
- Daily send: a GitHub Actions cron workflow (`.github/workflows/daily-quotes.yml`) runs the single-shot entrypoint `run_scheduled.py`. A timezone guard inside the entrypoint makes the 7 AM and 9 PM Eastern sends correct across daylight saving without a paid scheduler.

The legacy `server.js` (Express) and `backend/app.py` (Flask) are kept for reference only. The Netlify Functions replace them.

Why this stack: it removes the Replit dependency and every recurring cost. Static hosting, serverless functions, a serverless database, and a scheduled CI job all sit inside free tiers.

## How to run it yourself

You need a free Neon project and a free Resend account.

### 1. Database on Neon

1. Create a free project at [neon.tech](https://neon.tech/).
2. Copy the connection string (looks like `postgresql://...neon.tech/...?sslmode=require`). This is `DATABASE_URL`. The tables create themselves on first use.

### 2. Frontend and functions on Netlify

1. In Netlify, add a new site and import this repository.
2. Build settings come from `netlify.toml` (publish `frontend`, functions in `netlify/functions`). No build command is needed.
3. In Site settings, Environment variables, add `DATABASE_URL` (the Neon string).
4. Deploy. The subscribe form now writes real rows to Neon.

### 3. Daily send on GitHub Actions

1. In the repository, add Actions secrets (Settings, Secrets and variables, Actions):
   - `DATABASE_URL` (the Neon string)
   - `RESEND_API_KEY` (from [resend.com](https://resend.com/))
   - `SENDER_EMAIL` (a verified Resend sender, or `onboarding@resend.dev` for testing)
   - Twilio secrets are optional. Leave them unset for email-only.
2. The workflow runs on its cron automatically. To test now, run it manually from the Actions tab with the `slot` set to `morning`.

Sender note: `onboarding@resend.dev` is Resend's built-in test sender. It only delivers to the email address that owns the Resend account. To email real subscribers, verify a sending domain in Resend and set `SENDER_EMAIL` to an address on that domain.

## Project structure

```
DailyQuoteBlaster/
├── frontend/                   # static site published by Netlify
│   ├── index.html
│   ├── styles.css
│   └── scripts.js              # calls /api/subscribe and /api/quotes/recent
├── netlify/
│   └── functions/
│       ├── subscribe.mjs       # POST /api/subscribe, inserts a subscriber
│       └── recent-quotes.mjs   # GET /api/quotes/recent, returns recent sends
├── .github/workflows/
│   └── daily-quotes.yml        # cron: runs run_scheduled.py at 7 AM and 9 PM ET
├── run_scheduled.py            # single-shot send entrypoint (timezone guard)
├── main.py                     # core quote selection logic
├── send_email.py               # Resend email delivery
├── send_sms.py                 # Twilio SMS delivery (disabled by default)
├── database.py                 # Postgres connection and queries
├── quotes.json                 # quote collection
├── quotes_categories.json      # categorized quotes
├── netlify.toml                # Netlify build and functions config
├── .env.example                # environment variable template
├── docs/                       # PRD, technical spec, test cases
├── server.js                   # legacy Express server (unused)
└── backend/app.py              # legacy Flask server (unused)
```

## Local development

1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in `DATABASE_URL`, `RESEND_API_KEY`, and `SENDER_EMAIL`. The `.env` file is gitignored and must never be committed.
3. Install Python dependencies (the project uses `pyproject.toml` and `uv.lock`):
   ```
   pip install psycopg2-binary python-dotenv resend schedule twilio
   ```
4. Send one quote immediately for a local test:
   ```
   python run_scheduled.py morning
   ```

## Testing

For a full set of use cases and step-by-step test cases anyone can run against the live site, see [docs/test-cases.md](docs/test-cases.md). It covers subscribing through the form, checking the recent-quotes API, and triggering a manual send.
