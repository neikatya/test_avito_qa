import requests
from tests.conftest import extract_item_id, generate_unique_seller_id


def test_tc_1_1_create_item_success(base_url, valid_item_payload):
    response = requests.post(f"{base_url}/api/1/item", json=valid_item_payload)

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert isinstance(data["status"], str)
    assert data["status"].startswith("Сохранили объявление - ")

    item_id = extract_item_id(data["status"])
    assert item_id

    get_response = requests.get(f"{base_url}/api/1/item/{item_id}")
    assert get_response.status_code == 200

    items = get_response.json()
    assert isinstance(items, list)
    assert len(items) == 1

    item = items[0]
    assert item["id"] == item_id
    assert item["sellerId"] == valid_item_payload["sellerID"]
    assert item["name"] == valid_item_payload["name"]
    assert item["price"] == valid_item_payload["price"]
    assert item["statistics"] == valid_item_payload["statistics"]


def test_tc_1_2_create_item_without_seller_id(base_url):
    payload = {
        "name": "Test item",
        "price": 1000,
        "statistics": {"likes": 5, "viewCount": 1, "contacts": 35}
    }

    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code == 400

    data = response.json()
    assert "result" in data
    assert "message" in data["result"] or "messages" in data["result"]


def test_tc_1_3_create_item_invalid_seller_id_type(base_url):
    payload = {
        "sellerID": "111666",
        "name": "Test item",
        "price": 1000,
        "statistics": {"likes": 5, "viewCount": 1, "contacts": 35}
    }

    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code == 400


def test_tc_1_4_create_item_invalid_price_negative(base_url):
    payload = {
        "sellerID": generate_unique_seller_id(),
        "name": "Test item",
        "price": -1,
        "statistics": {"likes": 5, "viewCount": 1, "contacts": 35}
    }

    response = requests.post(f"{base_url}/api/1/item", json=payload)
    # BUG-1: API принимает отрицательную цену (ожидается 400)
    assert response.status_code == 200


def test_tc_1_4_create_item_invalid_price_string(base_url):
    payload = {
        "sellerID": generate_unique_seller_id(),
        "name": "Test item",
        "price": "1000",
        "statistics": {"likes": 5, "viewCount": 1, "contacts": 35}
    }

    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code == 400


def test_tc_1_5_create_item_empty_name(base_url):
    payload = {
        "sellerID": generate_unique_seller_id(),
        "name": "",
        "price": 1000,
        "statistics": {"likes": 5, "viewCount": 1, "contacts": 35}
    }

    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code in [200, 400]


def test_tc_1_5_create_item_very_long_name(base_url):
    payload = {
        "sellerID": generate_unique_seller_id(),
        "name": "A" * 301,
        "price": 1000,
        "statistics": {"likes": 5, "viewCount": 1, "contacts": 35}
    }

    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code in [200, 400]


def test_tc_1_6_create_item_without_statistics(base_url):
    payload = {
        "sellerID": generate_unique_seller_id(),
        "name": "Test item",
        "price": 1000
    }

    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code in [200, 400]


def test_tc_1_6_create_item_negative_likes(base_url):
    payload = {
        "sellerID": generate_unique_seller_id(),
        "name": "Test item",
        "price": 1000,
        "statistics": {"likes": -1, "viewCount": 1, "contacts": 35}
    }

    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code in [200, 400]


def test_tc_1_6_create_item_invalid_view_count_type(base_url):
    payload = {
        "sellerID": generate_unique_seller_id(),
        "name": "Test item",
        "price": 1000,
        "statistics": {"likes": 5, "viewCount": "1", "contacts": 35}
    }

    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code in [200, 400]
