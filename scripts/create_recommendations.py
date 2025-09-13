import httpx
from tests.data.recommendation_sequences_samples import RECOMMENDATIONS_SEQUENCES_SAMPLES


def main() -> None:
    host = "http://127.0.0.1:8000"

    samples = list(RECOMMENDATIONS_SEQUENCES_SAMPLES) + [
        ((1293, 9128, 19923), []),
        ((392, 324023, 40234), []),
        ((13, 24, 2323, 5435, 34534, 2342), []),
        ((13, 24, 2323, 5435, 34534, 2342), []),
    ]
    with httpx.Client() as client:
        response = client.post(f"{host}/api/v1/auth/login", json={"username": "admin", "password": "admin"}).json()
        access_token = response["access_token"]

        for sample in samples:
            print(sample[0])

            endpoint = f"{host}/api/v1/recommendations/"
            headers = {"Authorization": f"Bearer {access_token}"}
            payload = {"product_ids": sample[0]}
            response = client.post(endpoint, headers=headers, json=payload).json()
            print(f"Response: {response}")


if __name__ == "__main__":
    main()
