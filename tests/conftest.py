import re
import random
import pytest
import requests


BASE_URL = "https://qa-internship.avito.com"


def extract_item_id(status_string):
    match = re.search(r"[0-9a-fA-F-]{36}", status_string)
    if match:
        return match.group(0)
    raise ValueError(f"Cannot extract UUID from: {status_string}")


def generate_unique_seller_id():
    return random.randint(111111, 999999)


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def valid_item_payload():
    return {
        "sellerID": generate_unique_seller_id(),
        "name": "Test item",
        "price": 1000,
        "statistics": {
            "likes": 5,
            "viewCount": 1,
            "contacts": 35
        }
    }


@pytest.fixture
def created_item(base_url, valid_item_payload):
    response = requests.post(f"{base_url}/api/1/item", json=valid_item_payload)
    assert response.status_code == 200

    data = response.json()
    item_id = extract_item_id(data["status"])

    return {
        "item_id": item_id,
        "seller_id": valid_item_payload["sellerID"],
        "payload": valid_item_payload
    }


@pytest.fixture
def created_items_for_seller(base_url):
    seller_id = generate_unique_seller_id()
    item_ids = []

    for i in range(2):
        payload = {
            "sellerID": seller_id,
            "name": f"Test item {i+1}",
            "price": 1000 + i * 100,
            "statistics": {
                "likes": i + 1,
                "viewCount": (i + 1) * 2,
                "contacts": (i + 1) * 3
            }
        }

        response = requests.post(f"{base_url}/api/1/item", json=payload)
        assert response.status_code == 200

        item_id = extract_item_id(response.json()["status"])
        item_ids.append(item_id)

    return {
        "seller_id": seller_id,
        "item_ids": item_ids
    }
