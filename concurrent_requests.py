from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests import adapters

URL = "https://k6yd10lkx7.execute-api.ap-south-1.amazonaws.com/purchase"

session = requests.Session()
adapter = adapters.HTTPAdapter(
    pool_connections=200,
    pool_maxsize=200
)
session.mount("https://", adapter)


def call_api():
    try:
        print("Purchasing iPhone17....")
        r = session.post(URL, timeout=5)
        return r.status_code
    except Exception as e:
        return str(e)


results = []

with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(call_api) for _ in range(100)]

    for f in as_completed(futures):
        results.append(f.result())

success = results.count(200)
sold_out = results.count(409)
errors = len(results) - success - sold_out

print("===============")
print("Success:", success)
print("Sold out:", sold_out)
print("Errors:", errors)
print("Total:", len(results))
print("===============")
