# CSRF Vulnerability Crawler and Research

This repository is a small, focused project for understanding and testing Cross-Site Request Forgery (CSRF) issues in a controlled environment. It combines research notes, a lightweight crawler, and a simple proof-of-concept (PoC) to demonstrate how these vulnerabilities appear in practice.

---

## What’s inside

* Notes on how CSRF works and how frameworks handle it
* A crawler that scans pages for possible CSRF weaknesses
* A minimal HTML PoC for lab-based demonstrations

---

## Legal notice

Use this project only on applications you own or have explicit permission to test.

Do not run this against live systems, production environments, or third-party applications without authorization.

---

## CSRF basics

CSRF (Cross-Site Request Forgery) happens when a browser is tricked into sending a request to a site where the user is already authenticated.

Since browsers automatically include cookies, the server may accept the request as legitimate—even though the user never intended it.

Typical impact:

* Changing account details
* Triggering transactions
* Performing privileged actions silently

---

## Why protection matters

Any request that changes state (POST, PUT, DELETE, etc.) must be verified.

Without proper validation:

* The server trusts the browser blindly
* Attackers can execute actions through the victim’s session

---

## How CSRF protection works

Most defenses rely on validating that the request is intentional.

### Token-based validation

A CSRF token should:

* Be unpredictable
* Be tied to the user session or verifiable server-side
* Be required for every state-changing request

If the token is missing or invalid, the request should fail.

---

## Common protection methods

* **Synchronizer token pattern**
  Token stored on the server and embedded in forms

* **Double submit cookie**
  Token sent in both cookie and request, then compared

* **SameSite cookies**
  Limits when cookies are sent in cross-site requests

* **Origin / Referer checks**
  Ensures the request comes from a trusted source

* **Re-authentication**
  Used for high-risk actions

---

## Middleware examples

* Django: `CsrfViewMiddleware`
* Express.js: custom middleware or libraries
* Spring Security: built-in CSRF protection
* Laravel: automatic CSRF token validation

---

## CSRF crawler

The crawler is designed to flag areas that *might* be vulnerable. It does not exploit anything—it only highlights suspicious patterns.

### What it looks for

* Forms using POST/PUT/DELETE without visible CSRF tokens
* Missing hidden input fields that resemble tokens
* JavaScript requests (`fetch`, `XMLHttpRequest`) that look state-changing
* Absence of common CSRF headers

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

Basic scan:

```bash
python crawler.py --url http://localhost:8000 --max-pages 30
```

Save results to a file:

```bash
python crawler.py --url http://localhost:8000 --output findings.json
```

---

## Output

The crawler typically reports:

* Pages visited
* Forms detected
* Endpoints that may lack CSRF protection
* Notes on why something was flagged

This is heuristic-based, so results should always be verified manually.

---

## HTML PoC (lab use only)

The `poc.html` file is a simple demonstration of how a CSRF attack might look.

It works by:

* Creating a hidden form
* Submitting it automatically
* Sending a request using the victim’s session

---

## How to use the PoC

1. Open `poc.html`

2. Replace placeholders:

   * target URL
   * parameter names
   * parameter values

3. Make sure:

   * You are logged into the target app
   * The app is intentionally vulnerable (test environment only)

---

## Example

```html
<form action="TARGET_URL" method="POST">
  <input type="hidden" name="email" value="attacker@example.com">
</form>

<script>
  document.forms[0].submit();
</script>
```

Optional: hide the page to make it less visible during testing

```html
<style>
  body {
    display: none;
  }
</style>
```

---

## Project structure

```
.
├── crawler.py
├── requirements.txt
├── poc.html
├── README.md
└── research/
```

---

## Contributing

If you want to contribute, keep it relevant to the goal of the project.

Useful contributions include:

* Adding modern CSRF scenarios (AJAX, APIs, etc.)
* Improving crawler detection logic
* Adding defensive examples
* Improving documentation

### Basic workflow

```bash
git checkout -b feature/your-change
git commit -m "Add: short description of change"
git push origin feature/your-change
```

Then open a pull request with a clear explanation.

---

## Notes

* This project is for learning and testing only
* The crawler is not a full security scanner
* Always verify findings manually

---

## Summary

This repo is meant to help you:

* Understand how CSRF works
* Identify weak implementations
* See how an attack is constructed

All in a controlled and responsible setup.
