import httpx


def main() -> None:
    host = "http://127.0.0.1:8000"

    with httpx.Client() as client:
        response = client.post(f"{host}/api/v1/auth/login", json={"username": "admin", "password": "admin"}).json()
        access_token = response["access_token"]

        list_endpoint = f"{host}/api/v1/recommendations/"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(list_endpoint, headers=headers).json()
        for recommendation in response:
            print(recommendation)


if __name__ == "__main__":
    main()
