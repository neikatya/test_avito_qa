import uuid
import requests


def test_tc_2_1_get_existing_item(base_url, created_item):
    item_id = created_item["item_id"]
    payload = created_item["payload"]

    response = requests.get(f"{base_url}/api/1/item/{item_id}")
    assert response.status_code == 200

    items = response.json()
    assert isinstance(items, list)
    assert len(items) == 1

    item = items[0]
    assert "id" in item
    assert "sellerId" in item
    assert "name" in item
    assert "price" in item
    assert "statistics" in item
    assert "createdAt" in item

    assert item["id"] == item_id
    assert item["sellerId"] == payload["sellerID"]
    assert item["name"] == payload["name"]
    assert item["price"] == payload["price"]
    assert item["statistics"] == payload["statistics"]


def test_tc_2_2_get_nonexistent_item(base_url):
    nonexistent_id = str(uuid.uuid4())
    response = requests.get(f"{base_url}/api/1/item/{nonexistent_id}")
    assert response.status_code == 404


def test_tc_2_3_get_item_with_empty_id(base_url):
    response = requests.get(f"{base_url}/api/1/item/")
    assert response.status_code in [400, 404]


def test_tc_2_3_get_item_with_invalid_id(base_url):
    response = requests.get(f"{base_url}/api/1/item/abc")
    assert response.status_code in [400, 404]
