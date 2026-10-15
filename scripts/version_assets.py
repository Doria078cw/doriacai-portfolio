#!/usr/bin/env python3
"""Give local CSS/JS references content versions before publishing static pages."""
from hashlib import sha256
from pathlib import Path
import re
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = re.compile(r'(?P<attr>\b(?:href|src)=)(?P<quote>[\"\'])(?P<url>[^\"\']+)(?P=quote)')


def version_reference(match, page):
    url = urlsplit(match['url'])
    if url.scheme or url.netloc or not url.path.endswith(('.css', '.js')):
        return match.group(0)
    target = (ROOT / unquote(url.path.lstrip('/'))) if url.path.startswith('/') else (page.parent / unquote(url.path)).resolve()
    if not target.is_file():
        raise FileNotFoundError(f'{page.relative_to(ROOT)}: {url.path}')
    version = sha256(target.read_bytes()).hexdigest()[:12]
    query = [(key, value) for key, value in parse_qsl(url.query) if key != 'v']
    query.append(('v', version))
    updated = urlunsplit((url.scheme, url.netloc, url.path, urlencode(query), url.fragment))
    return f"{match['attr']}{match['quote']}{updated}{match['quote']}"


if __name__ == '__main__':
    changed = 0
    for page in sorted(ROOT.rglob('*.html')):
        if any(part.startswith('.') for part in page.relative_to(ROOT).parts):
            continue
        original = page.read_text()
        updated = REFERENCE.sub(lambda match: version_reference(match, page), original)
        if original != updated:
            page.write_text(updated)
            changed += 1
    print(f'Updated asset versions in {changed} HTML pages.')
