import requests
from tests.conftest import generate_unique_seller_id


def test_tc_3_1_get_seller_items(base_url, created_items_for_seller):
    seller_id = created_items_for_seller["seller_id"]
    created_ids = created_items_for_seller["item_ids"]

    response = requests.get(f"{base_url}/api/1/{seller_id}/item")
    assert response.status_code == 200

    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 2

    for item in items:
        assert item["sellerId"] == seller_id

    returned_ids = [item["id"] for item in items]
    for created_id in created_ids:
        assert created_id in returned_ids


def test_tc_3_2_get_seller_items_no_items(base_url):
    new_seller_id = generate_unique_seller_id()
    response = requests.get(f"{base_url}/api/1/{new_seller_id}/item")

    assert response.status_code == 200

    items = response.json()
    assert isinstance(items, list)
    assert len(items) == 0


def test_tc_3_3_get_seller_items_invalid_seller_id_string(base_url):
    response = requests.get(f"{base_url}/api/1/abc/item")
    assert response.status_code in [400, 404]


def test_tc_3_3_get_seller_items_out_of_range(base_url):
    response = requests.get(f"{base_url}/api/1/1000000/item")
    assert response.status_code in [200, 400, 404]
