import requests
from bs4 import BeautifulSoup, Tag


def _clone(out_soup: BeautifulSoup, tag: Tag) -> Tag:
  """Clone a tag into out_soup."""
  return BeautifulSoup(str(tag), 'html.parser').find()  # type: ignore


def _strip_attrs(root: Tag, keep=('href',)):
  for t in root.find_all(True):
    for a in list(t.attrs.keys()):
      if a not in keep:
        del t.attrs[a]


def _remove_citations(root: Tag):
  for sup in root.select('sup.reference'):
    sup.decompose()


def clean_wikipedia_html(html: str) -> str:
  soup = BeautifulSoup(html, 'html.parser')

  h1 = soup.select_one('h1#firstHeading')
  content = soup.select_one('div.mw-parser-output')
  if not h1 or not content:
    raise ValueError(
      'Expected Wikipedia structure not found (h1#firstHeading, div.mw-parser-output).'
    )

  # Output doc
  out = BeautifulSoup(
    "<!doctype html><html><head><meta charset='utf-8'></head><body></body></html>",
    'html.parser',
  )
  body = out.body

  # Add H1
  h1_copy = _clone(out, h1)
  _remove_citations(h1_copy)
  _strip_attrs(h1_copy, keep=())
  body.append(h1_copy)  # type: ignore

  # Find all H2s in the main content (Wikipedia sections)
  h2s = content.find_all('h2', recursive=True)

  # --- Lead paragraphs (before first h2) ---
  first_h2 = h2s[0] if h2s else None
  if first_h2:
    for p in content.find_all('p', recursive=True):
      if p.get_text(strip=True) == '':
        continue
      # Only keep <p> that appear before the first h2 in document order
      if p.sourceline and first_h2.sourceline and p.sourceline >= first_h2.sourceline:
        # sourceline can be None depending on parser; see fallback below
        continue

    # Fallback that works even when sourceline is None:
    for el in content.descendants:
      if isinstance(el, Tag) and el is first_h2:
        break
      if isinstance(el, Tag) and el.name == 'p' and el.get_text(strip=True):
        p_copy = _clone(out, el)
        _remove_citations(p_copy)
        _strip_attrs(p_copy, keep=('href',))
        body.append(p_copy)  # type: ignore
  else:
    # No h2 at all: keep all paragraphs
    for p in content.find_all('p', recursive=True):
      if p.get_text(strip=True):
        p_copy = _clone(out, p)
        _remove_citations(p_copy)
        _strip_attrs(p_copy, keep=('href',))
        body.append(p_copy)  # type: ignore

  # --- Sections (h2 + all following p until next h2) ---
  for idx, h2 in enumerate(h2s):
    title = h2.get_text(' ', strip=True)
    if title.strip().lower() == 'references':
      break

    # Add H2
    h2_copy = _clone(out, h2)
    _remove_citations(h2_copy)
    _strip_attrs(h2_copy, keep=())
    body.append(h2_copy)  # type: ignore

    # Collect <p> after this h2 until the next h2
    next_h2 = h2s[idx + 1] if idx + 1 < len(h2s) else None

    # Walk forward in document order from this h2
    for el in h2.next_elements:
      if not isinstance(el, Tag):
        continue

      # Stop when we reach the next section heading
      if next_h2 is not None and el is next_h2:
        break

      # Only collect paragraphs that are still inside the main content
      if el.name == 'p' and el.get_text(strip=True) and content in el.parents:
        p_copy = _clone(out, el)
        _remove_citations(p_copy)
        _strip_attrs(p_copy, keep=('href',))
        body.append(p_copy)  # type: ignore

  return str(out)


if __name__ == '__main__':
  import os
  import random
  import time

  import requests

  url = os.environ.get('URL', 'https://en.wikipedia.org/wiki/Kubernetes')
  min_wait = int(os.environ.get('MIN_WAIT', '0'))
  max_wait = int(os.environ.get('MAX_WAIT', '0'))
  volume_path = os.environ.get('VOLUME_PATH', './')
  is_init = True if min_wait == 0 and max_wait == 0 else False

  headers = {
    'User-Agent': 'wiki-replicator-bot/1.0 (+https; educational; rate <1req/5min)'
  }

  full_path = os.path.join(volume_path, 'index.html')

  if min_wait > max_wait:
    raise Exception(f'Invalid time range {min_wait}m - {max_wait}m')

  while True:
    if not is_init:
      rand_num = random.randint(min_wait, max_wait)  # thundering herd proof?
      time.sleep(rand_num * 60)

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    html = resp.text

    cleaned = clean_wikipedia_html(html)
    with open(full_path, 'w', encoding='utf-8') as f:
      f.write(cleaned)

    print(f'Successfully parsed and wrote the cleaned html for {url}')

    if is_init:
      break
