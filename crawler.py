import argparse
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

TOKEN_HINTS = (
    "csrf",
    "token",
    "xsrf",
    "authenticity",
    "requestverificationtoken",
    "_token",
)

STATE_CHANGING_METHODS = {"post", "put", "patch", "delete"}


def has_csrf_token(form) -> bool:
    for field in form.find_all(["input", "meta"]):
        name = (field.get("name") or "").lower()
        field_id = (field.get("id") or "").lower()
        value = (field.get("value") or "").lower()
        combined = f"{name} {field_id} {value}"
        if any(hint in combined for hint in TOKEN_HINTS):
            return True
    return False


def scan_page(url: str, timeout: int = 10):
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    forms = soup.find_all("form")

    if not forms:
        print(f"[-] No forms found on {url}")
        return

    for index, form in enumerate(forms, start=1):
        method = (form.get("method") or "get").strip().lower()
        action = form.get("action") or url
        action_url = urljoin(url, action)

        # Skip read-only forms.
        if method not in STATE_CHANGING_METHODS:
            continue

        if has_csrf_token(form):
            print(
                f"[+] Protected form found | page={url} | form=#{index} | method={method.upper()} | action={action_url}"
            )
        else:
            print(
                f"[!] Vulnerable form found | page={url} | form=#{index} | method={method.upper()} | action={action_url}"
            )


def main():
    parser = argparse.ArgumentParser(
        description="CSRF Vulnerability Crawler (local lab use only)"
    )
    parser.add_argument("url", help="Target URL (example: http://127.0.0.1:5000)")
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="HTTP request timeout in seconds",
    )
    args = parser.parse_args()

    parsed = urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        raise SystemExit("Invalid URL. Use a full URL like http://127.0.0.1:5000")

    scan_page(args.url, args.timeout)


if __name__ == "__main__":
    main()
