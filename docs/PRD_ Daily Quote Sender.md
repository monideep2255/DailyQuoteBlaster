# **📌 PRD: Daily Quote Sender – Charge-Up Edition**

**Version:** Full Detail — May 2025

---

## Current status (July 2026)

This is the original May 2025 planning document, kept for history. The app shipped and was later migrated off Replit to a fully free serverless stack. For the current architecture and how to run it, see [../README.md](../README.md) and [test-cases.md](test-cases.md).

What changed since this document was written:

- Email is Resend, not SendGrid.
- The daily send runs on a GitHub Actions cron job, not Replit or Windsurf cron.
- The app now has database persistence (Neon serverless Postgres, tables `subscribers` and `quotes_sent`). The "no database persistence" non-goal below no longer holds.
- The web APIs are Netlify Functions, not an always-on Express or Flask backend.
- Live site: https://dailyquoteblaster.netlify.app

---

## **1\. 🧠 Background / Context**

Many people want a small ritual to start their day with intention, energy, or calm. While journaling and meditation apps exist, they often require user interaction. A lightweight solution is to receive a **daily motivational or thoughtful quote** in the morning — no app required.

The **Daily Quote Sender (Charge-Up Edition)** is a personal or sharable tool that randomly selects a quote from a predefined list and sends it via **email** (or optionally SMS) each morning. This builds a positive habit loop, requires no user input, and runs entirely in the background.

---

## **2\. ❗ Problem Statement**

* People want daily inspiration or motivation but don’t want another app to open.

* Existing quote apps are noisy, ad-filled, or require interaction.

* Users prefer simple tools that work passively, reliably, and privately.

---

## **3\. ✅ Solution Overview**

**Daily Quote Sender** is a set-it-and-run micro-tool. It:

* Picks a quote from a pre-uploaded or hardcoded list

* Sends one email (or SMS) per day

* Runs automatically (via Windsurf or Replit cron)

* Can be hosted with a small UI or used as a personal routine tool

---

## **4\. 🔧 Feature Development Phases**

### **✨ Phase 1: MVP (Email Delivery)**

* Load a static list of quotes

* Randomly pick 1 each day

* Send via email (SendGrid)

* Triggered by a scheduler (Replit cron or Windsurf)

### **📱 Phase 2: Optional SMS Support**

* Use Twilio API to send the same quote via text

* Add user config for delivery type

### **🌐 Phase 3: Frontend UI (Optional)**

* Display recent quotes or archive

* “Subscribe” input (email only)

* Public Netlify-hosted microsite

---

## **5\. 📅 Example Use Cases**

* “Send me a quote every weekday at 7:30 AM to start the day.”

* “Let me upload my own quote list to use instead of default ones.”

* “I want to send this to my team as a ritual.”

---

## **6\. 👤 User Personas**

* 🧘 Individual seeking a daily moment of mindfulness

* 💼 Manager who wants to uplift their team daily

* 🎨 Creator who wants to publish a quote series

---

## **7\. 🧠 AI Strategy (Optional Later)**

Not in MVP. Future phases could explore:

* GPT-curated quotes by topic or mood

* AI-generated original affirmations

* Sentiment-aware delivery

---

## **8\. 📊 Success Metrics**

* Quote delivered successfully each day

* Open rates or reply counts (if tracked)

* SMS delivery success (if added)

* Time-to-launch (goal: 5 days max)

---

## **9\. 📂 Stack / Dependencies**

* Email: **SendGrid (free tier)**

* SMS: **Twilio (optional, free tier)**

* Scheduler: **Windsurf or Replit cron**

* Hosting (if UI): **Netlify**

* Backend: Replit (Node or Python)

---

## **10\. 🚫 Non-Goals**

* No user authentication

* No AI quote personalization (MVP)

* No database persistence

* No mobile app

