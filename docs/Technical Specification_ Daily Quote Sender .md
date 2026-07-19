# **🛠 Technical Specification: Daily Quote Sender – Charge-Up Edition**

**Version:** v1.0 — May 2025

---

## Current status (July 2026): architecture as built

This v1.0 spec is the original May 2025 design, kept for history. The app was built and then migrated off Replit to a free serverless stack. The as-built architecture differs from the plan below:

- Frontend: static site in `frontend/`, hosted on Netlify.
- APIs: two Netlify Functions (`subscribe`, `recent-quotes`) using `@neondatabase/serverless` with parameterized queries. They replace the planned Flask and Express backend.
- Database: Neon serverless Postgres, tables `subscribers` and `quotes_sent`, auto-created on first use. (The "no database" security note below no longer applies; email addresses are stored.)
- Email: Resend, not SendGrid.
- Scheduling: a GitHub Actions cron workflow (`.github/workflows/daily-quotes.yml`) runs `run_scheduled.py` at 7 AM and 9 PM Eastern, with an internal timezone guard for daylight saving. It replaces Replit and Windsurf cron.
- SMS: Twilio code is present but disabled (email-only, no cost).

For setup steps and tests, see [../README.md](../README.md) and [test-cases.md](test-cases.md). Live site: https://dailyquoteblaster.netlify.app

---

## **1\. 📅 Application Overview**

The Daily Quote Sender is a backend-driven, schedule-based tool that randomly selects a quote from a local list and sends it to a recipient via email (and optionally SMS) every morning. The system is designed to be minimal, reliable, and shareable.

---

## **2\. ⚙️ Architecture Overview**

**Backend**

* Language: Python (preferred) or Node.js

* Logic:

  * Load list of quotes (JSON or array in file)

  * Use randomizer to select one quote

  * Format into a message template

  * Send via SendGrid (or Twilio for SMS)

  * Trigger daily via cron (Replit or Windsurf)

**Frontend**

* Static UI (HTML or React) to show archive and allow subscriptions

* Host on Netlify

* “Subscribe” input (stores local email list)

**Deployment Options**

* **Development:** Replit (backend testing)

* **Production:** Replit cron job or Windsurf task

* **UI Deployment:** Netlify (static page)

---

## **3\. 🔄 Data Flow**

1. At scheduled time (e.g., 7:30 AM):

2. Trigger function loads quote list → picks random quote

3. Formats email body

4. Sends via SendGrid (email) or Twilio (SMS)

5. Logs delivery (console or file for MVP)

---

## **4\. 📄 File Structure (MVP Version)**

daily-quote/  
├── quotes.json  
├── send\_email.py  
├── scheduler.py (or cron.json)  
├── .env (API keys)  
├── requirements.txt / package.json  
├── README.md  
├── backend/  
│   ├── app.py  
│   ├── requirements.txt  
├── frontend/  
│   ├── index.html  
│   ├── styles.css  
│   └── scripts.js  
└── docs/  
    └── Technical Specification_ Daily Quote Sender .md

---

## **5\. ✅ MVP Milestones**

| Phase | Deliverable |
| ----- | ----- |
| 1 | Send one daily quote via email using static quote list |
| 2 | Add SMS option via Twilio |
| 3 | Deploy static quote archive (Netlify) |
| 4 | Implement frontend UI for displaying quotes and handling subscriptions |

---

## **6\. 🔒 Security & Privacy**

* No user data stored (no auth or database)

* Environment variables store API keys

* Minimal logging, no PII

* Free-tier usage (SendGrid, Twilio limits respected)

---

## **7\. 📜 Dependencies**

* Python:

  * `sendgrid` or `smtplib`

  * `schedule`, `random`, `dotenv`

  * `Flask`, `Flask-Cors`

* Node.js:

  * `@sendgrid/mail`, `cron`, `dotenv`

* Deployment:

  * Replit, Windsurf for scheduling

  * Netlify for UI

---

## **8\. 🧪 Testing Plan**

* Manual test: run script locally → confirm email delivery

* Integration test: check randomizer pulls valid quote

* Scheduler test: cron executes properly

* Fallback test: if quote list is empty, send default fallback

* Frontend test: confirm subscription form works and recent quotes are displayed

---

## **9\. 🧩 Extensions / Future Work**

* Topic/tag support (filter by category)

* Multi-user delivery

* AI-based quote selection (mood-based)

* UI to upload custom quote lists

---

## **10\. 🌐 Hosting Frontend on Netlify**

1. Create a Netlify account if you don't have one.

2. Connect your GitHub repository to Netlify.

3. Deploy the `frontend` directory as a static site.

4. Configure the build settings if necessary (e.g., build command, publish directory).

5. After deployment, your frontend UI will be accessible via the Netlify URL provided.

