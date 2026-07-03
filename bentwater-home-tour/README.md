# Bentwater Holiday Home Tour — Task Manager

An elegant, single-file dashboard for tracking the Bentwater Holiday Home Tour committee plan — themed after the arched stone mansion entrance at Christmas (deep stone, velvet red, brass gold, cream, flocked evergreen).

## Features

- **Dashboard** — live metrics (complete / in progress / blocked / overdue), overall completion bar, progress by month, next deadlines
- **Tasks** — the full committee plan (Jan–July prep through the January wrap-up), filterable and searchable, with editable owners, due dates, status pills, and notes; overdue items auto-flag in red
- **Homes · Volunteers · Tickets · Budget · Contacts** — one tab per section of the binder, all editable in place
- **✦ Guide Me** — a step-by-step spotlight walkthrough of the whole app (auto-offers on first visit; also available from the floating button)
- **Autosave** — everything persists in the browser (localStorage); **Export / Import Data** moves a JSON snapshot between teammates or machines

## Run locally

No build step, no dependencies — just open the file:

```
open bentwater-home-tour/index.html        # macOS
# or double-click index.html in any browser
```

Or serve it:

```
npx serve bentwater-home-tour
```

## Deploy to Netlify

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop)
2. Drag the `bentwater-home-tour` folder onto the page
3. Done — share the URL with the committee

> Note: data is saved per-browser. Teammates on the shared URL each keep their own working copy; use **Export Data → Import Data** to pass the authoritative snapshot around, or ask for a synced backend later.
