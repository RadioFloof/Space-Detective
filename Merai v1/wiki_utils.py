import requests
import html
import re

def get_object_image_url(name):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if 'thumbnail' in data and 'source' in data['thumbnail']:
                return data['thumbnail']['source']
    except Exception:
        pass
    return None

def get_object_description(name):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if 'extract' in data:
                return html.unescape(data['extract'])
    except Exception:
        pass
    return None

def extract_name_from_description(description: str) -> str | None:
    """Extracts the first capitalized word from a description, likely a name."""
    if not description:
        return None
    
    # Match a capitalized word, possibly with hyphens or numbers
    match = re.match(r"([A-Z][a-zA-Z0-9\\-]{2,})", description)
    if match:
        potential_name = match.group(1)
        # Avoid generic words if possible by checking length or a blacklist if needed
        if len(potential_name) > 2: # Simple check to avoid very short words
            return potential_name
    return None
