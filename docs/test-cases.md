# Use cases and test cases

How to try the Daily Quote Sender and confirm each part works. Live site: https://dailyquoteblaster.netlify.app

## Contents

- [Use cases](#use-cases)
- [Test cases for anyone](#test-cases-for-anyone)
- [Test cases for maintainers](#test-cases-for-maintainers)
- [Reference: API and categories](#reference-api-and-categories)

## Use cases

- A visitor wants a daily quote by email and subscribes through the form.
- A visitor wants to see what quotes were recently sent.
- A subscriber picks which categories and which times (morning, evening) they want.
- A maintainer wants to send a quote on demand to confirm delivery works.

## Test cases for anyone

You only need a web browser. No account or login.

### TC1: Subscribe through the form

1. Open https://dailyquoteblaster.netlify.app
2. Enter your email in the subscribe form.
3. Select at least one delivery time (morning or evening).
4. Optionally select categories. If you pick none, you get all of them.
5. Submit.

Expected: a success message like "Subscription successful! You will receive your first quote soon."

Note on delivery: the live site currently uses Resend's test sender (`onboarding@resend.dev`), which only delivers email to the address that owns the project's Resend account. If you subscribe with your own email, your row is saved but you will not receive mail until a sending domain is verified. The subscribe step itself still succeeds and is the part this test checks.

### TC2: See recent quotes on the page

1. On the same page, find the recent quotes section.
2. If no quotes have been sent yet, a small sample is shown so the page is not empty.

Expected: the section renders quote cards with text, author, and category.

### TC3: Call the recent-quotes API directly

Run this in a terminal:

```bash
curl -s https://dailyquoteblaster.netlify.app/api/quotes/recent
```

Expected: a JSON array of objects with `text`, `author`, `date`, and `category`.

### TC4: Subscribe through the API

```bash
curl -s -X POST https://dailyquoteblaster.netlify.app/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","deliveryTimes":{"morning":true,"evening":false},"categories":["motivational"]}'
```

Expected: `{"success":true,"message":"Subscription successful! ...","id":<number>}`

### TC5: Validation, bad input is rejected

Missing delivery time:

```bash
curl -s -X POST https://dailyquoteblaster.netlify.app/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","deliveryTimes":{"morning":false,"evening":false}}'
```

Expected: HTTP 400 with `"Select at least one delivery time."`

Invalid email:

```bash
curl -s -X POST https://dailyquoteblaster.netlify.app/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"not-an-email","deliveryTimes":{"morning":true}}'
```

Expected: HTTP 400 with `"That email address looks invalid."`

Wrong method (GET instead of POST):

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://dailyquoteblaster.netlify.app/api/subscribe
```

Expected: `405`.

## Test cases for maintainers

These need access to the GitHub repository and the Neon database.

### TC6: Trigger a manual send

From the repository Actions tab, run the "Daily quote send" workflow with `slot` set to `morning`. Or from the command line:

```bash
gh workflow run daily-quotes.yml --repo <owner>/DailyQuoteBlaster --ref main -f slot=morning
```

Expected: the run completes with success.

### TC7: Confirm the send wrote a row

Query Neon:

```bash
psql "$DATABASE_URL" -c "SELECT id, subscriber_id, quote_author, category, delivery_method, time_of_day, sent_at FROM quotes_sent ORDER BY id DESC LIMIT 5;"
```

Expected: a new `quotes_sent` row with `delivery_method = email` and a recent `sent_at`.

### TC8: Confirm a subscriber was saved

```bash
psql "$DATABASE_URL" -c "SELECT id, email, morning_delivery, evening_delivery, active FROM subscribers ORDER BY id DESC LIMIT 5;"
```

Expected: the subscriber you added in TC1 or TC4 appears.

### TC9: Confirm the email arrived

If the recipient is the Resend account owner's address, check that inbox for a "Daily Quote" email from `onboarding@resend.dev`. This is the only address the test sender can reach.

## Reference: API and categories

Endpoints:

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/subscribe` | Add a subscriber |
| GET | `/api/quotes/recent` | List recent sent quotes |

Subscribe body fields:

- `email` (string) or `phone` (string): at least one is required.
- `deliveryTimes`: object with `morning` and `evening` booleans. At least one must be true.
- `categories`: array from the list below. Empty means all.

Categories: `general`, `motivational`, `wisdom`, `growth`, `decisions`, `success`.
