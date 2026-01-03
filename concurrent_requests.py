import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "https://v6uucolola.execute-api.ap-south-1.amazonaws.com/prod/book"

def send_request(i):
    try:
        r = requests.post(API_URL, timeout=5)
        return r.status_code
    except Exception as e:
        return str(e)

def main():
    results = []

    with ThreadPoolExecutor(max_workers=1000) as executor:
        futures = [executor.submit(send_request, i) for i in range(1000)]

        for future in as_completed(futures):
            results.append(future.result())

    success = results.count(200)
    sold_out = results.count(409)

    print(f"Success: {success}")
    print(f"Sold out: {sold_out}")
    print(f"Total: {len(results)}")

if __name__ == "__main__":
    main()
