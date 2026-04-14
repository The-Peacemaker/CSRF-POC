import argparse
import json
import re
from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


TOKEN_HINTS = {
    "csrf",
    "token",
    "xsrf",
    "authenticity_token",
    "_token",
    "requestverificationtoken",
}

HEADER_HINTS = {
    "x-csrf-token",
    "x-xsrf-token",
    "x-requested-with",
}


def is_same_origin(base_url: str, candidate_url: str) -> bool:
    base = urlparse(base_url)
    candidate = urlparse(candidate_url)
    return (base.scheme, base.netloc) == (candidate.scheme, candidate.netloc)


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    fragmentless = parsed._replace(fragment="")
    return fragmentless.geturl()


def find_forms_without_token(soup: BeautifulSoup, page_url: str):
    findings = []
    forms = soup.find_all("form")

    for idx, form in enumerate(forms, start=1):
        method = (form.get("method") or "get").strip().lower()
        if method == "get":
            continue

        token_found = False
        inputs = form.find_all(["input", "meta"])
        for element in inputs:
            name = (element.get("name") or "").lower()
            element_id = (element.get("id") or "").lower()
            value = (element.get("value") or "").lower()
            joined = f"{name} {element_id} {value}"
            if any(hint in joined for hint in TOKEN_HINTS):
                token_found = True
                break

        if not token_found:
            action = form.get("action") or page_url
            findings.append(
                {
                    "type": "missing_csrf_form_token",
                    "page": page_url,
                    "form_index": idx,
                    "method": method.upper(),
                    "action": action,
                    "risk": "high",
                    "note": "State-changing form appears to lack an obvious CSRF token field.",
                }
            )

    return findings


def find_js_state_change_without_header(html_text: str, page_url: str):
    findings = []

    # Heuristic: detect fetch/ajax calls that use POST/PUT/PATCH/DELETE.
    js_patterns = [
        r"fetch\([^\)]*method\s*:\s*['\"](POST|PUT|PATCH|DELETE)['\"]",
        r"\$\.ajax\([^\)]*type\s*:\s*['\"](POST|PUT|PATCH|DELETE)['\"]",
        r"axios\.(post|put|patch|delete)\(",
    ]

    state_change_detected = any(
        re.search(pattern, html_text, flags=re.IGNORECASE | re.DOTALL)
        for pattern in js_patterns
    )

    if not state_change_detected:
        return findings

    lowered = html_text.lower()
    header_present = any(header in lowered for header in HEADER_HINTS)

    if not header_present:
        findings.append(
            {
                "type": "possible_missing_csrf_header",
                "page": page_url,
                "risk": "medium",
                "note": "State-changing JS request patterns found without obvious CSRF header usage.",
            }
        )

    return findings


def extract_links(soup: BeautifulSoup, page_url: str, base_url: str):
    links = set()
    for a in soup.find_all("a", href=True):
        absolute = normalize_url(urljoin(page_url, a["href"]))
        if is_same_origin(base_url, absolute):
            links.add(absolute)
    return links


def crawl(start_url: str, max_pages: int, timeout: int):
    visited = set()
    queue = deque([normalize_url(start_url)])
    session = requests.Session()
    findings = []

    while queue and len(visited) < max_pages:
        current = queue.popleft()
        if current in visited:
            continue

        visited.add(current)
        try:
            response = session.get(current, timeout=timeout)
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type.lower():
                continue
        except requests.RequestException as exc:
            findings.append(
                {
                    "type": "crawl_error",
                    "page": current,
                    "risk": "info",
                    "note": f"Request failed: {exc}",
                }
            )
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        findings.extend(find_forms_without_token(soup, current))
        findings.extend(find_js_state_change_without_header(response.text, current))

        for link in extract_links(soup, current, start_url):
            if link not in visited:
                queue.append(link)

    return findings, visited


def main():
    parser = argparse.ArgumentParser(
        description="Defensive CSRF crawler for authorized security testing."
    )
    parser.add_argument("--url", required=True, help="Start URL, e.g. http://localhost:8000")
    parser.add_argument("--max-pages", type=int, default=20, help="Maximum pages to crawl")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout in seconds")
    parser.add_argument("--output", help="Optional path to JSON findings")
    args = parser.parse_args()

    findings, visited = crawl(args.url, args.max_pages, args.timeout)

    summary = {
        "start_url": args.url,
        "pages_visited": len(visited),
        "findings_count": len(findings),
        "findings": findings,
    }

    print(json.dumps(summary, indent=2))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fp:
            json.dump(summary, fp, indent=2)
        print(f"\nSaved findings to {args.output}")


if __name__ == "__main__":
    main()
