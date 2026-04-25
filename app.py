from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = "lab-secret-key-change-me"

DASHBOARD_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Profile Dashboard - Vulnerable Lab</title>
  <style>
    :root {
      --bg-1: #f5f1e8;
      --bg-2: #e3dccd;
      --panel: #fffdfa;
      --ink: #1f2a33;
      --accent: #bb3e03;
      --accent-2: #005f73;
      --line: #d7ccb8;
      --ok: #2a9d8f;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: "Segoe UI", Tahoma, sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at 10% 10%, rgba(187, 62, 3, 0.08), transparent 25%),
        radial-gradient(circle at 90% 90%, rgba(0, 95, 115, 0.1), transparent 30%),
        linear-gradient(135deg, var(--bg-1), var(--bg-2));
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 24px;
    }

    .card {
      width: min(860px, 100%);
      border: 1px solid var(--line);
      border-radius: 18px;
      overflow: hidden;
      background: var(--panel);
      box-shadow: 0 16px 34px rgba(0, 0, 0, 0.08);
    }

    .top {
      padding: 22px 26px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }

    .badge {
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 700;
      background: rgba(42, 157, 143, 0.14);
      color: var(--ok);
    }

    .grid {
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 0;
    }

    .left,
    .right {
      padding: 24px 26px;
    }

    .left {
      border-right: 1px solid var(--line);
    }

    h1 {
      margin: 0;
      font-size: clamp(1.2rem, 3vw, 1.6rem);
    }

    h2 {
      margin: 0 0 14px;
      font-size: 1.04rem;
    }

    .meta {
      margin-top: 14px;
      display: grid;
      gap: 10px;
    }

    .meta .row {
      display: flex;
      justify-content: space-between;
      padding-bottom: 8px;
      border-bottom: 1px dashed var(--line);
      gap: 12px;
    }

    .meta .row strong {
      color: #5b6973;
      font-weight: 600;
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 600;
      font-size: 0.92rem;
    }

    input[type="text"] {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 12px;
      font-size: 0.98rem;
      margin-bottom: 12px;
    }

    button {
      border: none;
      border-radius: 10px;
      background: linear-gradient(90deg, var(--accent), #ca6702);
      color: #fff;
      padding: 11px 16px;
      font-weight: 700;
      cursor: pointer;
    }

    .warn {
      margin-top: 14px;
      background: rgba(187, 62, 3, 0.08);
      color: #8d2b02;
      border-left: 4px solid var(--accent);
      padding: 10px 12px;
      font-size: 0.9rem;
    }

    .flash {
      margin: 12px 26px 0;
      border-radius: 10px;
      background: rgba(0, 95, 115, 0.09);
      color: var(--accent-2);
      padding: 10px 12px;
      font-size: 0.9rem;
      font-weight: 600;
    }

    @media (max-width: 760px) {
      .grid {
        grid-template-columns: 1fr;
      }

      .left {
        border-right: none;
        border-bottom: 1px solid var(--line);
      }
    }
  </style>
</head>
<body>
  <main class="card">
    <header class="top">
      <h1>Account Dashboard</h1>
      <span class="badge">Lab Session Active</span>
    </header>

    {% if updated %}
      <div class="flash">Profile updated successfully.</div>
    {% endif %}

    <section class="grid">
      <article class="left">
        <h2>Current Profile</h2>
        <div class="meta">
          <div class="row"><strong>Username</strong><span>{{ username }}</span></div>
          <div class="row"><strong>Email</strong><span>{{ username|lower|replace(' ', '.') }}@lab.local</span></div>
          <div class="row"><strong>Role</strong><span>Research Student</span></div>
          <div class="row"><strong>Last Action</strong><span>Profile Name Update</span></div>
        </div>
      </article>

      <article class="right">
        <h2>Update Display Name</h2>
        <form action="{{ url_for('update_profile') }}" method="post">
          <label for="display_name">Display name</label>
          <input id="display_name" name="display_name" type="text" value="{{ username }}" required />
          <button type="submit">Save Changes</button>
        </form>
        <div class="warn">
          Intentionally vulnerable endpoint for CSRF demonstration. No anti-CSRF token validation is implemented.
        </div>
      </article>
    </section>
  </main>
</body>
</html>
"""


@app.before_request
def seed_session_user() -> None:
    if "username" not in session:
        session["username"] = "Alice"


@app.get("/")
def index():
    updated = request.args.get("updated") == "1"
    return render_template_string(
        DASHBOARD_TEMPLATE,
        username=session["username"],
        updated=updated,
    )


@app.post("/update-profile")
def update_profile():
    # Deliberately vulnerable: accepts authenticated cookie-backed POST without CSRF token checks.
    new_name = request.form.get("display_name", "").strip()
    if new_name:
        session["username"] = new_name
    return redirect(url_for("index", updated=1))


if __name__ == "__main__":
    app.run(debug=True)
