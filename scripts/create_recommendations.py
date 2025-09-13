import httpx


def main() -> None:
    host = "http://127.0.0.1:8000"

    samples = [
        (1293, 9128, 19923),
        (392, 324023, 40234),
        (13, 24, 2323, 5435, 34534, 2342),
        (13, 24, 2323, 5435, 34534, 2342),
        (1,),
        (1, 2),
        (1, 2, 3),
        (2, 4, 6),
        (1, 2, 3, 4),
        (1, 2, 3, 4, 5),
        (2, 3, 5, 7),
        (10, 20, 30, 40, 50),
        (1, 3, 5, 7, 9, 11),
    ]
    with httpx.Client() as client:
        response = client.post(f"{host}/api/v1/auth/login", json={"username": "admin", "password": "admin"}).json()
        access_token = response["access_token"]

        for sample in samples:
            endpoint = f"{host}/api/v1/recommendations/"
            headers = {"Authorization": f"Bearer {access_token}"}
            payload = {"product_ids": sample}
            response = client.post(endpoint, headers=headers, json=payload).json()
            print(f"Response: {response}")


if __name__ == "__main__":
    main()
