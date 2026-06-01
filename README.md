# Randoms

Collect the photos your friends took when you weren't looking.

Randoms is a photo-sharing web app built around life events. Create an occasion, share a link, and everyone adds their candid photos with a few words. No app to download. Guests never need an account. Your wall builds itself.

---

## What it does

- Create an occasion (graduation, birthday, wedding — anything worth remembering)
- Share a link to your WhatsApp group
- Guests upload photos and a caption — no login required
- You approve each photo before it appears on your wall
- Your wall is a permanent, private archive of who you were

Over time it becomes a life archive. Every occasion stacked up over years. And one day, when it matters most, the people you love get to keep you.

---

## Tech stack

| Layer       | Choice                  |
|-------------|-------------------------|
| Backend     | Flask (Python)          |
| Database    | PostgreSQL via Supabase  |
| File storage| Cloudflare R2           |
| Auth        | Google OAuth (Authlib)  |
| Frontend    | HTMX + vanilla CSS      |
| Deployment  | Render                  |

No JavaScript framework. No external CSS framework. Flask returns HTML fragments. HTMX swaps them in. That's it.

---

## Project structure

```
randoms/
├── app.py              # Flask app factory, config, blueprint registration
├── models.py           # SQLAlchemy models — User, Event, Photo, Comment
├── storage.py          # Cloudflare R2 client — the only file that touches R2
├── routes/
│   ├── auth.py         # Google OAuth login, callback, logout
│   ├── events.py       # Dashboard, create occasion, wall, approval queue
│   └── uploads.py      # Guest upload page and upload handler
├── templates/
│   ├── base.html       # Master layout — navbar, sidebar, bottom nav
│   ├── homepage.html   # Landing page (logged-out)
│   ├── dashboard.html  # Creator home
│   ├── new_occasion.html
│   ├── share_link.html
│   ├── upload.html     # Guest upload (no login)
│   ├── wall.html       # Social feed of approved photos
│   ├── approvals.html  # Pending photo queue
│   ├── settings.html
│   └── fragments/      # HTMX partial responses
├── static/
│   ├── style.css       # All CSS — one file, no framework
│   ├── manifest.json   # PWA manifest
│   ├── sw.js           # Service worker
│   └── icons/
│       ├── icon-192.png
│       └── icon-512.png
├── .env                # Secrets — never committed
├── requirements.txt
└── Procfile
```

---

## Getting started locally

**1. Clone and create a virtual environment**

```bash
git clone https://github.com/yourusername/randoms.git
cd randoms
python -m venv venv
source venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Set up your `.env` file**

```
SECRET_KEY=your-long-random-string
DATABASE_URL=postgresql://...
R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
R2_BUCKET_NAME=randoms-photos
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

**4. Run the app**

```bash
flask run
```

Visit `http://localhost:5000`

---

## Environment variables

| Variable              | What it is                                      |
|-----------------------|-------------------------------------------------|
| `SECRET_KEY`          | Long random string for Flask session security   |
| `DATABASE_URL`        | PostgreSQL connection string (Supabase)         |
| `R2_ENDPOINT_URL`     | Cloudflare R2 endpoint from R2 dashboard        |
| `R2_ACCESS_KEY_ID`    | R2 API token access key                         |
| `R2_SECRET_ACCESS_KEY`| R2 API token secret                             |
| `R2_BUCKET_NAME`      | Your R2 bucket name                             |
| `GOOGLE_CLIENT_ID`    | From Google Cloud Console OAuth credentials     |
| `GOOGLE_CLIENT_SECRET`| From Google Cloud Console OAuth credentials     |

---

## Build phases

| Phase | Goal                              | Status      |
|-------|-----------------------------------|-------------|
| 1     | Core loop — upload → wall         | In progress |
| 2     | Creator controls — auth, approvals| Not started |
| 3     | Ship to real users                | Not started |
| 4     | Shareable cards, scan old photos  | Not started |
| 5     | Legacy / AI tribute feature       | Not started |

---

## Key rules that never change

1. Guests never sign up — name field only, no email, no password
2. Comments are mandatory — a photo without words is not a memory
3. Creators approve before photos go live
4. Photos are stored in Cloudflare R2 — never on the Flask server
5. The wall never deletes — photos are permanent unless the owner removes them
6. Personal walls are private — group walls are visible to anyone with the link

---

## Deployment

The app deploys to Render via the `Procfile`:

```
web: gunicorn app:app
```

Connect your GitHub repo in the Render dashboard, add your environment variables, and it deploys automatically on every push to `main`.
