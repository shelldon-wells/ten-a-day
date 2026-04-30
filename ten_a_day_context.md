# Ten a Day — Project Context Document
*Upload this file when starting a new chat to continue building this app.*

---

## 1. Project Overview

Ten a Day is a web-based daily to-do list application. The core concept is simple: each user can have a maximum of 10 active tasks at any time. Tasks persist until the user completes them — there is no automatic daily reset. Completing a task deletes it permanently. Incomplete tasks carry over indefinitely.

---

## 2. Core App Rules

- Each user can have a maximum of 10 active tasks at any time.
- Completing a task deletes it permanently — there is no history or archive.
- Incomplete tasks carry over to the next day automatically (they simply stay on the list).
- Each user only sees their own tasks (private per account).
- No streaks, no history, no task archive — keep it simple.

---

## 3. Technology Stack

| Component        | Choice                                      |
|------------------|---------------------------------------------|
| Language         | Python 3                                    |
| Framework        | Flask                                       |
| Database         | Google Firestore (NoSQL, cloud-hosted)      |
| Authentication   | Google OAuth 2.0 (Google Sign-In)           |
| Hosting          | Google Cloud Run                            |
| Dev OS           | Ubuntu (local development machine)          |
| Dependency mgmt  | pip + virtual environment (venv)            |

---

## 4. Step-by-Step Build Plan

- **Step 1 (DONE):** Set up project folder & virtual environment
- **Step 2 (DONE):** Create a basic Flask app that shows a webpage
- **Step 3 (DONE):** Set up Google Cloud project & connect Firestore
- **Step 4 (DONE):** Understand the data model & do a test write to Firestore
- **Step 5 (DONE):** Set up Google OAuth so users can sign in
- **Step 6 (DONE):** Build the main to-do page (add, complete & delete tasks)
- **Step 7 (DONE):** Style it up with CSS
- **Step 8 (DONE):** Make the app a PWA
- **Step 9 (DONE):** Deploy to Google Cloud Run
- **Step 10 (DONE):** Set up environment variables & push to GitHub

---

## 5. What Was Completed — Steps 1–10

### Step 1 — Project Setup
- Folder created: `~/ten-a-day/`
- Virtual environment created and activated: `source venv/bin/activate`
- Packages installed: `flask`, `google-auth`, `google-auth-oauthlib`, `google-cloud-firestore`, `firebase-admin`, `authlib`
- Dependencies saved to: `requirements.txt`

### Step 2 — Basic Flask App
- `app.py` created in `~/ten-a-day/`
- Single route (`/`) returns a confirmation string
- Runs with: `python app.py` (debug mode on)

### Step 3 — Google Cloud & Firestore
- Google Cloud project created: `ten-a-day-494607`
- Firestore database created in Native mode (region: `europe-west1`)
- Service account created with **Cloud Datastore User** role
- JSON key downloaded and saved as: `~/ten-a-day/serviceAccountKey.json`
- `.gitignore` created excluding `serviceAccountKey.json` and `venv/`
- `app.py` updated to initialise Firebase and create a Firestore client (`db`)
- Connection confirmed working (no errors on startup)

### Step 4 — Firestore Data Model & Test Write
- Confirmed the Firestore data structure works end to end
- Learned the difference between collections, documents, and subcollections
- `firestore.client()` requires `database_id=` argument (not `database=`) in firebase-admin 7.4.0
- The correct Firestore client initialisation is: `db = firestore.client(database_id=os.environ.get("DATABASE_NAME"))`
- A temporary `/test-write` route was added to `app.py`, tested successfully, then removed
- `firebase-admin` upgraded to version 7.4.0

### Step 5 — Google OAuth
- OAuth consent screen created in Google Cloud Console (External, published to production)
- OAuth 2.0 Client ID created (Web application, named "Ten a Day Web")
- Authorised redirect URIs set to:
  - `http://localhost:5000/callback` (local development)
  - `https://ten-a-day-717280198396.europe-west1.run.app/callback` (production)
- `authlib` installed and added to `requirements.txt`
- `app.py` updated with login, callback, and logout routes
- Sign-in flow tested and confirmed working
- **Known quirk:** The `scope` parameter must be passed explicitly to `google.authorize_redirect()`, not just in the `oauth.register()` call

### Step 6 — Main To-Do Page
- `templates/` folder created at `~/ten-a-day/templates/`
- `templates/tasks.html` created with Jinja2 templating
- Tasks are displayed in a list with a task count (e.g. "2 / 10")
- Add task form is shown when task count is below 10; a limit message is shown at 10
- Completing a task POSTs to `/complete/<task_id>` and permanently deletes the Firestore document
- All three routes confirmed working end-to-end

### Step 7 — CSS Styling
- `static/` folder created at `~/ten-a-day/static/`
- `static/style.css` created with a dark mode design
- `templates/login.html` created — a styled sign-in page (replaces the old plain-text link)
- `templates/tasks.html` updated to link the stylesheet and use CSS class names
- `app.py` updated to render `login.html` via `render_template()` instead of returning a raw string
- All pages confirmed working and visually consistent

### Step 8 — PWA
- `static/manifest.json` created with app name, colours, and icon references
- `static/icons/` folder created
- `static/icons/icon-192.png` and `icon-512.png` generated using Pillow (dark background with "10" in white)
- `static/sw.js` created — service worker that caches app files for offline use
- Both `login.html` and `tasks.html` updated to link the manifest and register the service worker
- PWA confirmed working in Chrome DevTools (manifest, service worker, and cache all green)

### Step 9 — Deploy to Google Cloud Run
- `gcloud` and `docker` confirmed installed
- Logged in to gcloud with correct Google account
- Project set to `ten-a-day-494607`
- Cloud Run and Cloud Build APIs enabled
- `Dockerfile` created
- `.dockerignore` created — excludes `venv/`, `serviceAccountKey.json`, `__pycache__/`, etc.
- `app.py` updated — Flask now reads `PORT` from environment, listens on `0.0.0.0`, debug mode off
- `app.py` updated — Firebase initialisation now uses Application Default Credentials (ADC) on Cloud Run, falls back to `serviceAccountKey.json` locally
- `ProxyFix` middleware added — fixes `http://` vs `https://` mismatch caused by Cloud Run's proxy
- Cloud Run service account granted `roles/datastore.user` permission for Firestore access
- App deployed successfully via `gcloud run deploy`
- OAuth consent screen published to production
- Live URL confirmed working: `https://ten-a-day-717280198396.europe-west1.run.app`

### Step 10 — Environment Variables & GitHub
- `python-dotenv` installed and added to `requirements.txt`
- `.env` file created locally with all sensitive values (`SECRET_KEY`, `DATABASE_NAME`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`)
- `app.py` updated to read all sensitive values from environment variables via `os.environ.get()`
- Environment variables set in Cloud Run via `gcloud run services update --set-env-vars`
- `.env` and `client_secret_*.json` added to `.gitignore` and removed from git tracking
- Git repository initialised and code committed
- SSH key generated and added to GitHub
- Remote set to: `git@github.com:shelldon-wells/ten-a-day.git`
- Code pushed to GitHub successfully — no secrets in the repository

---

## 6. Current File Contents

### app.py
```python
import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, session, render_template, request
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

if os.path.exists("serviceAccountKey.json"):
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app()

db = firestore.client(database_id=os.environ.get("DATABASE_NAME"))

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@app.route("/")
def index():
    user = session.get("user")
    if not user:
        return render_template("login.html")

    tasks_ref = db.collection("users").document(user["id"]).collection("tasks")
    tasks_snapshot = tasks_ref.order_by("created_at").get()

    tasks = []
    for doc in tasks_snapshot:
        task = doc.to_dict()
        task["id"] = doc.id
        tasks.append(task)

    return render_template("tasks.html", user=user, tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    user = session.get("user")
    if not user:
        return redirect(url_for("index"))

    tasks_ref = db.collection("users").document(user["id"]).collection("tasks")

    existing = tasks_ref.get()
    if len(existing) >= 10:
        return redirect(url_for("index"))

    title = request.form.get("title", "").strip()
    if not title:
        return redirect(url_for("index"))

    tasks_ref.add({
        "title": title,
        "created_at": firestore.SERVER_TIMESTAMP,
    })

    return redirect(url_for("index"))

@app.route("/complete/<task_id>", methods=["POST"])
def complete_task(task_id):
    user = session.get("user")
    if not user:
        return redirect(url_for("index"))

    task_ref = db.collection("users").document(user["id"]).collection("tasks").document(task_id)
    task_ref.delete()

    return redirect(url_for("index"))

@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)
    return google.authorize_redirect(redirect_uri, scope="openid email profile")

@app.route("/callback")
def callback():
    token = google.authorize_access_token()
    user_info = token["userinfo"]
    session["user"] = {
        "id": user_info["sub"],
        "name": user_info["name"],
        "email": user_info["email"],
    }
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
```

---

### .env (local only — never commit this file)
```
SECRET_KEY=your-actual-secret-key
DATABASE_NAME=your-actual-database-name
GOOGLE_CLIENT_ID=your-actual-client-id
GOOGLE_CLIENT_SECRET=your-actual-client-secret
```

---

### templates/login.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Ten a Day</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  <link rel="manifest" href="/static/manifest.json">
</head>
<body>

  <div class="container">

    <header>
      <h1>Ten a Day</h1>
    </header>

    <p class="task-count">A simple daily task list. Ten tasks. No clutter.</p>

    <a href="/login" class="btn-signin">Sign in with Google</a>

  </div>

  <script>
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/static/sw.js");
    }
  </script>

</body>
</html>
```

---

### templates/tasks.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Ten a Day</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  <link rel="manifest" href="/static/manifest.json">
</head>
<body>

  <div class="container">

    <header>
      <h1>Ten a Day</h1>
      <a href="/logout" class="logout-link">Logout</a>
    </header>

    <p class="task-count">{{ tasks | length }} / 10 tasks</p>

    {% if tasks | length < 10 %}
      <form action="/add" method="POST" class="add-form">
        <input type="text" name="title" placeholder="What needs doing?" required>
        <button type="submit" class="btn-add">Add</button>
      </form>
    {% else %}
      <p class="limit-message">You've hit the 10 task limit. Complete something first!</p>
    {% endif %}

    {% if tasks %}
      <ul class="task-list">
        {% for task in tasks %}
          <li class="task-item">
            <span class="task-title">{{ task.title }}</span>
            <form action="/complete/{{ task.id }}" method="POST">
              <button type="submit" class="btn-done">✓ Done</button>
            </form>
          </li>
        {% endfor %}
      </ul>
    {% else %}
      <p class="empty-message">No tasks yet. You're all clear!</p>
    {% endif %}

  </div>

  <script>
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/static/sw.js");
    }
  </script>

</body>
</html>
```

---

### static/manifest.json
```json
{
  "name": "Ten a Day",
  "short_name": "Ten a Day",
  "description": "A simple daily task list. Ten tasks. No clutter.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#121212",
  "theme_color": "#121212",
  "icons": [
    {
      "src": "/static/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

---

### static/sw.js
```javascript
const CACHE_NAME = "ten-a-day-v1";
const URLS_TO_CACHE = [
  "/",
  "/static/style.css",
  "/static/manifest.json",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(URLS_TO_CACHE);
    })
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request);
    })
  );
});
```

---

### static/style.css
```css
/* ── Reset & base ── */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  background-color: #121212;
  color: #e0e0e0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  padding: 3rem 1rem;
}

.container {
  width: 100%;
  max-width: 540px;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 2rem;
}

h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.5px;
}

.logout-link {
  font-size: 0.85rem;
  color: #888;
  text-decoration: none;
}

.logout-link:hover {
  color: #e0e0e0;
}

.task-count {
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 1.2rem;
}

.add-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.add-form input[type="text"] {
  flex: 1;
  background-color: #1e1e1e;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  color: #e0e0e0;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.add-form input[type="text"]:focus {
  border-color: #555;
}

.add-form input[type="text"]::placeholder {
  color: #555;
}

.btn-add {
  background-color: #2a2a2a;
  color: #e0e0e0;
  border: 1px solid #444;
  border-radius: 8px;
  padding: 0.6rem 1.1rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-add:hover {
  background-color: #333;
}

.limit-message {
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 2rem;
}

.task-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1e1e1e;
  border: 1px solid #2a2a2a;
  border-radius: 10px;
  padding: 0.75rem 1rem;
}

.task-title {
  font-size: 1rem;
  color: #e0e0e0;
}

.btn-done {
  background: none;
  border: 1px solid #444;
  border-radius: 6px;
  color: #888;
  padding: 0.3rem 0.7rem;
  font-size: 0.85rem;
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s;
  white-space: nowrap;
}

.btn-done:hover {
  border-color: #6dbf7e;
  color: #6dbf7e;
}

.empty-message {
  color: #555;
  font-size: 0.95rem;
  margin-top: 1rem;
}

.btn-signin {
  display: inline-block;
  margin-top: 1.5rem;
  background-color: #1e1e1e;
  color: #e0e0e0;
  border: 1px solid #444;
  border-radius: 8px;
  padding: 0.65rem 1.3rem;
  font-size: 1rem;
  text-decoration: none;
  transition: background-color 0.2s, border-color 0.2s;
}

.btn-signin:hover {
  background-color: #2a2a2a;
  border-color: #666;
}
```

---

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT=8080

CMD ["python", "app.py"]
```

---

### .dockerignore
```
venv/
serviceAccountKey.json
__pycache__/
*.pyc
.env
.gitignore
```

---

### .gitignore
```
venv/
serviceAccountKey.json
__pycache__/
*.pyc
.env
client_secret_*.json
```

---

## 7. Firestore Data Structure (Confirmed Working)

```
users/                          ← collection
  {google_user_id}/             ← document (one per user)
    email: "user@gmail.com"
    name: "Jane"
    tasks/                      ← subcollection
      {task_id}/                ← document (one per task)
        title: "Buy groceries"
        created_at: <timestamp>
```

- Tasks are private — nested under each user's document.
- No task history. Completing a task deletes its document permanently.
- Maximum 10 task documents per user at any time.
- `firestore.SERVER_TIMESTAMP` is used for `created_at` (server-side time, not local).

---

## 8. Key Decisions Already Made

| Topic            | Decision                                                                 |
|------------------|--------------------------------------------------------------------------|
| Database         | Firestore chosen over PostgreSQL — easier setup, free tier, Google-native |
| Hosting          | Google Cloud Run — user already has a Google Cloud account               |
| No SQL needed    | Firestore is NoSQL (document-based), no SQLAlchemy required              |
| Task completion  | Completing a task deletes it, it is not simply marked as done            |
| No history       | No task history, archive, or streaks feature                             |
| Carry-over       | Unfinished tasks stay on the list until completed                        |
| Open source only | User prefers open source tools only (e.g. plain text/markdown over docx) |
| Step-by-step     | User wants to learn — explain every line of code                         |
| Ask before next  | Always ask the user before moving to the next step                       |
| database_id      | Must pass `database_id=` explicitly to `firestore.client()` — the default does not auto-resolve in this project |
| OAuth scope      | Must pass `scope="openid email profile"` explicitly to `google.authorize_redirect()` — passing it only in `oauth.register()` is not sufficient |
| PWA              | App is a PWA — manifest, service worker, and icons all confirmed working in Chrome DevTools |
| Credentials      | `serviceAccountKey.json` is excluded from Docker image — Cloud Run uses Application Default Credentials (ADC) instead |
| ProxyFix         | `werkzeug.middleware.proxy_fix.ProxyFix` must be applied to fix `http://` vs `https://` mismatch behind Cloud Run's proxy |
| Secret key       | Flask secret key generated with `secrets.token_hex(32)` and stored as environment variable |
| Environment vars | All sensitive values stored in `.env` locally and set via `gcloud run services update --set-env-vars` in production |
| GitHub auth      | SSH key authentication used for GitHub — HTTPS with PAT did not work reliably |

---

## 9. Deployment & Repository Details

| Item | Value |
|------|-------|
| Google Cloud project ID | `ten-a-day-494607` |
| Cloud Run region | `europe-west1` |
| Live URL | `https://ten-a-day-717280198396.europe-west1.run.app` |
| GitHub repository | `git@github.com:shelldon-wells/ten-a-day.git` |

---

## 10. Development Workflow

When making changes to the app:

**1. Make and test changes locally:**
```bash
cd ~/ten-a-day
source venv/bin/activate
python app.py
```

**2. Commit and push to GitHub:**
```bash
git add .
git commit -m "description of change"
git push
```

**3. Redeploy to Cloud Run:**
```bash
gcloud run deploy ten-a-day \
  --source . \
  --region europe-west1 \
  --platform managed \
  --allow-unauthenticated
```

**4. If environment variables have changed, update them in Cloud Run:**
```bash
gcloud run services update ten-a-day \
  --region europe-west1 \
  --set-env-vars SECRET_KEY="...",DATABASE_NAME="...",GOOGLE_CLIENT_ID="...",GOOGLE_CLIENT_SECRET="..."
```

---

## 11. How to Continue Building This App

- Always explain what each line of code does — the user is learning.
- Do NOT paste the entire app at once — build one step at a time.
- After completing a step, ask the user if they have questions before moving on.
- The user is on Ubuntu — all terminal commands should be Linux/bash.
- The active virtual environment command is: `source venv/bin/activate`
- The project folder is: `~/ten-a-day/`
- User prefers open source tools only — avoid proprietary formats like .docx.
- After any code changes, follow the development workflow in Section 10.
