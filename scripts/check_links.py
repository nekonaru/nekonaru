"""Check that every image URL in README.md responds with HTTP < 400.

Standard library only. Run by GitHub Actions, or locally: python scripts/check_links.py
"""
import re
import sys
import urllib.request

README = "README.md"
TIMEOUT = 20
UA = "profile-link-checker"

# Markdown images: ![alt](url)
MD_IMAGE = re.compile(r"!\[[^\]]*\]\((https?://[^)\s]+)\)")
# HTML images: <img src="url">
HTML_IMAGE = re.compile(r'<img[^>]*?src="(https?://[^"]+)"')


def candidates(text):
    urls = set()
    urls.update(m for m in HTML_IMAGE.findall(text))
    urls.update(m for m in MD_IMAGE.findall(text))
    return sorted(urls)


def check(url):
    headers = {"User-Agent": UA, "Accept": "image/*,*/*"}
    req = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        if e.code in (405, 501):
            req = urllib.request.Request(url, headers=headers, method="GET")
            try:
                with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                    return resp.status
            except Exception as e2:
                return getattr(e2, "code", 0) or 0
        return e.code
    except Exception:
        return 0


def main():
    with open(README, encoding="utf-8") as f:
        urls = candidates(f.read())
    print(f"Checking {len(urls)} image URLs in {README}")
    failures = []
    for url in urls:
        status = check(url)
        ok = isinstance(status, int) and status < 400
        print(f"{'OK ' if ok else 'FAIL'} [{status}] {url}")
        if not ok:
            failures.append((url, status))
    if failures:
        print(f"\n{len(failures)} image URL(s) failing:")
        for url, status in failures:
            print(f"  [{status}] {url}")
        return 1
    print("All image URLs OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
