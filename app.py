import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, session, render_template, request
from authlib.integrations.flask_client import OAuth
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


# credentials
if os.path.exists("serviceAccountKey.json"):
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app()



# create the databse client
db = firestore.client(database_id=os.environ.get("DATABASE_NAME"))


# The authorisation section
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)



# app.route is adecorator, it tells flask that when someon visits the root url(/), it should run the function below
@app.route("/")
def index():
    user = session.get("user")
    if not user:
        return render_template("login.html")

    tasks_ref = db.collection("users").document(user["id"]).collection("tasks")
    
    # Sort by is_pinned (True first) then by date
    # Note: This will require a Composite Index in Firestore
    tasks_snapshot = tasks_ref.order_by("is_pinned", direction=firestore.Query.DESCENDING).order_by("created_at").get()

    tasks = []
    for doc in tasks_snapshot:
        task = doc.to_dict()
        task["id"] = doc.id
        # Handle existing tasks that don't have the field yet
        task["is_pinned"] = task.get("is_pinned", False)
        tasks.append(task)

    return render_template("tasks.html", user=user, tasks=tasks)


@app.route("/toggle_pin/<task_id>", methods=["POST"])
def toggle_pin(task_id):
    user = session.get("user")
    if not user:
        return redirect(url_for("index"))

    task_ref = db.collection("users").document(user["id"]).collection("tasks").document(task_id)
    task_doc = task_ref.get()

    if task_doc.exists:
        current_status = task_doc.to_dict().get("is_pinned", False)
        task_ref.update({"is_pinned": not current_status})

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



@app.route("/add", methods=["POST"])
def add_task():
    user = session.get("user")
    if not user:
        return redirect(url_for("index"))

    tasks_ref = db.collection("users").document(user["id"]).collection("tasks")

    # Enforce the 10 task limit on the server side too
    existing = tasks_ref.get()
    if len(existing) >= 10:
        return redirect(url_for("index"))

    title = request.form.get("title", "").strip()
    if not title:
        return redirect(url_for("index"))

    # Add the task with the new is_pinned field
    tasks_ref.add({
        "title": title,
        "created_at": firestore.SERVER_TIMESTAMP,
        "is_pinned": False  # <--- CRITICAL: New tasks must have this field
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



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))





# Only run this block if we are executing this file
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

