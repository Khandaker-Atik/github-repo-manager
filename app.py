from flask import Flask, render_template, session, jsonify, redirect, url_for, request
import os, requests
from flask_cors import CORS
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()


GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")
GITHUB_API = "https://api.github.com"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "change_this_secret")
CORS(app, origins=[FRONTEND_URL], supports_credentials=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/auth/login")
def login():
    redirect_uri = url_for("callback", _external=True)

    scope = "repo delete_repo"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}&scope={scope}"
    )

@app.route("/auth/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "No code provided", 400
    token_res = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": url_for("callback", _external=True),
        },
    )
    token = token_res.json().get("access_token")
    if not token:
        return "OAuth failed", 400
    session["access_token"] = token
    return redirect(url_for("home"))

def get_token():
    return session.get("access_token")

@app.route("/api/me")
def api_me():
    token = get_token()
    if not token:
        return jsonify({"error": "Not logged in"}), 401
    user = requests.get(f"{GITHUB_API}/user", headers={"Authorization": f"token {token}"}).json()
    return jsonify(user)

def sort_repos(repos, sort_by, order):
    reverse = (order == "desc")
    if sort_by == "name":
        repos = sorted(repos, key=lambda r: r.get("name", "").lower(), reverse=reverse)
    elif sort_by == "updated":
        repos = sorted(repos, key=lambda r: r.get("updated_at", ""), reverse=reverse)
    elif sort_by == "created":
        repos = sorted(repos, key=lambda r: r.get("created_at", ""), reverse=reverse)
    return repos

@app.route("/api/repos")
def get_repos():
    token = get_token()
    if not token:
        return jsonify([]), 401
    sort_by = request.args.get("sort_by", "updated")  # name, created, updated
    order = request.args.get("order", "desc")         # asc, desc
    r = requests.get(f"{GITHUB_API}/user/repos?per_page=100", headers={"Authorization": f"token {token}"})
    repos = r.json()
    repos = sort_repos(repos, sort_by, order)
    return jsonify(repos)

@app.route("/api/public-repos/<username>")
def get_public_repos(username):
    """Get public repositories for any GitHub user (no auth required)"""
    sort_by = request.args.get("sort_by", "updated")  # name, created, updated
    order = request.args.get("order", "desc")         # asc, desc
    
    # Fetch public repos from GitHub API (no authentication needed)
    r = requests.get(f"{GITHUB_API}/users/{quote(username)}/repos?per_page=100&type=public")
    
    if r.status_code == 404:
        return jsonify({"error": "User not found"}), 404
    elif r.status_code != 200:
        return jsonify({"error": "Failed to fetch repositories"}), r.status_code
    
    repos = r.json()
    repos = sort_repos(repos, sort_by, order)
    return jsonify(repos)

@app.route("/api/repo/<owner>/<repo>/visibility", methods=["PATCH"])
def change_repo_visibility(owner, repo):
    token = get_token()
    if not token:
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json(silent=True)
    if not data or "private" not in data:
        return jsonify({"error": "Missing 'private' field"}), 400
    payload = {"private": data["private"]}
    api_url = f"{GITHUB_API}/repos/{quote(owner)}/{quote(repo)}"
    res = requests.patch(
        api_url,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        },
        json=payload,
    )
    if res.status_code == 200:
        return jsonify({"success": True})
    return jsonify({"error": "Failed to update visibility", "details": res.json()}), res.status_code

@app.route("/api/repo/<owner>/<repo>/delete", methods=["DELETE"])
def delete_repo(owner, repo):
    token = get_token()
    if not token:
        return jsonify({"error": "Not logged in"}), 401
    api_url = f"{GITHUB_API}/repos/{quote(owner)}/{quote(repo)}"
    res = requests.delete(
        api_url,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        },
    )
    print("Delete status:", res.status_code, "Response:", res.text)
    if res.status_code in [204, 202]:
        return jsonify({"success": True})
    return jsonify({"error": "Failed to delete repository", "details": res.json()}), res.status_code

@app.route("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(port=8000, debug=True)