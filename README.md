# CSRF Vulnerability Crawler and Research

## Project Overview
This project demonstrates Cross-Site Request Forgery (CSRF) in a **local vulnerable lab** using:

- `app.py`: intentionally vulnerable Flask profile dashboard
- `poc.html`: attacker page that auto-submits a forged request
- `crawler.py`: CSRF form checker for missing token protections

The goal is educational: show how CSRF works, prove impact in a safe environment, and detect weak forms programmatically.

## 1) CSRF Research

### What is CSRF?
Cross-Site Request Forgery (CSRF) is a web vulnerability where a victim's browser sends an unwanted, authenticated request to a target site. If the victim is logged in, browser cookies/sessions may be automatically included, and the server can process the forged request as if it were legitimate.

### How CSRF Tokens Work
A CSRF token is a secret, unpredictable value tied to a user session (or signed by the server). For every state-changing request (for example `POST`), the server expects this token in the form body or a header.

Typical validation flow:
1. Server generates token and sends it to the legitimate page.
2. Browser submits token with the action request.
3. Server verifies token correctness and association to the session.
4. If token is missing/invalid, server rejects the request.

Because attacker pages cannot read protected tokens from the victim site (same-origin policy), forged requests fail when token checks are enforced.

### Common CSRF Protections
1. **CSRF tokens** (synchronizer token or double-submit cookie pattern)
2. **SameSite cookies** (`Lax` or `Strict`) to reduce cross-site cookie sending
3. **Origin/Referer validation** for state-changing requests
4. **Custom headers** (for APIs), such as `X-CSRF-Token`, validated server-side

## 2) Project Structure

```text
csrf-project/
 ├── app.py
 ├── crawler.py
 ├── poc.html
 ├── requirements.txt
 └── README.md
```

## 3) Setup and Run

### Prerequisites
- Python 3.9+

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run vulnerable Flask lab
```bash
python app.py
```
Open: `http://127.0.0.1:5000`

### Run crawler
```bash
python crawler.py http://127.0.0.1:5000
```
Expected output style:
- `[!] Vulnerable form found ...` (missing CSRF token)
- `[+] Protected form found ...` (token detected)


## 4) Screenshots Explanation (Before/After)

For submission, capture at least two screenshots:

1. **Before attack**
   - Dashboard shows original username (`Alice`)
   - No forged update performed yet

2. **After attack**
   - After opening `poc.html`, dashboard shows modified username (`Mallory (CSRF)`)
   - Confirms state change without user intent

Optional third screenshot:
- Terminal output from `crawler.py` showing `[!] Vulnerable form found ...`

## 5) Conclusion
This project shows that if a web application accepts authenticated state-changing requests without CSRF defenses, an attacker-controlled page can silently trigger unwanted actions. A secure implementation should combine CSRF tokens with browser and request-level checks (SameSite cookies, Origin/Referer checks, and custom headers where appropriate).

---

**Important:** Use only in an authorized local lab for educational research.
