import requests
import os
from urllib.parse import urljoin

API_URI = os.getenv("API_URI")
API_URL = os.getenv("API_URL")
RAND_URL = os.getenv("RAND_URL", "https://en.wikipedia.org/wiki/Special:Random")

def generate_url():
    # suspicous headers will not work?
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/115.0.0.0 Safari/537.36'
    }
    # i can't catch the redirect manually. switching to auto redirect
    res = requests.get(RAND_URL, allow_redirects=True, headers=headers)
    print("Requesting:", RAND_URL)
    print("Response code:", res.status_code)
    print("Headers:", res.headers)
    # location =  res.headers['location']
    # return urljoin(RAND_URL, location)
    return res.url

def add_to_todo(address):
    tag = f'<a href="{address}">Read this Wiki</a>'
    payload = {"item": tag}
    try:
        r = requests.post(f"{API_URL}{API_URI}", json=payload)
        return r.json()
    except Exception as e:
        return e

if __name__ == "__main__":
    redirect = generate_url()
    print(add_to_todo(redirect))
