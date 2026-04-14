# CSRF Vulnerability Crawler and Research

This repository contains:

1. Research notes on CSRF middleware and protections.
2. A defensive crawler that checks pages for potential CSRF weaknesses.
3. An Ancient-NeoBrutalism themed HTML PoC page for authorized, lab-only demonstrations.

## Important Legal Notice

Use this project only on applications you own or have explicit permission to test.
Do not run security tests on third-party systems without authorization.

## Step 1: CSRF Middleware and Protection Research

### What CSRF Is

Cross-Site Request Forgery (CSRF) is an attack where a victim's browser is tricked into making authenticated requests to a target site without the victim's intent.

### Why Token Validation Matters

CSRF token validation works by requiring a nonce/token that:

1. Is hard to guess.
2. Is tied to the user session (or validated cryptographically).
3. Is validated server-side for state-changing requests.

Without a valid token, the server should reject the request.

### Common CSRF Protections

1. Synchronizer token pattern (server stores token in session).
2. Double-submit cookie pattern (token in cookie and request body/header).
3. SameSite cookies (`Lax` or `Strict`) to reduce cross-site cookie sending.
4. Origin/Referer checking for sensitive requests.
5. Re-authentication or step-up auth for high-risk actions.

### Middleware Examples

1. Django: `CsrfViewMiddleware`.
2. Express.js: custom middleware or libraries implementing token checks.
3. Spring Security: built-in CSRF protection.
4. Laravel: CSRF middleware with hidden token fields.

## Step 2: CSRF Defensive Crawler

The crawler looks for:

1. HTML forms using non-GET methods without obvious CSRF token fields.
2. JavaScript fetch/XHR calls that look state-changing but do not include common CSRF headers.

### Install

```bash
pip install -r requirements.txt
```

### Usage

```bash
python crawler.py --url http://localhost:8000 --max-pages 30
```

Optional output to JSON:

```bash
python crawler.py --url http://localhost:8000 --output findings.json
```

## Step 3: HTML PoC (Lab Only)

Open `poc.html` and update the placeholders:

1. `TARGET_URL`
2. Field names and values

This file demonstrates how a forged form post could look in an intentionally vulnerable training environment.

## Step 4: Push to GitHub

```bash
git init
git add .
git commit -m "Add CSRF crawler research and themed PoC"
git branch -M main
git remote add origin https://github.com/The-Peacemaker/CSRF-POC
git push -u origin main
```

## Submission Hashtag

`#cl-cybersec-crawler`
