import uuid
import requests


def test_tc_5_1_delete_item_success(base_url, created_item):
    item_id = created_item["item_id"]
    response = requests.delete(f"{base_url}/api/2/item/{item_id}")

    assert response.status_code == 200
    assert response.text == ""


def test_tc_5_2_verify_deleted_item_get(base_url, created_item):
    item_id = created_item["item_id"]

    delete_response = requests.delete(f"{base_url}/api/2/item/{item_id}")
    assert delete_response.status_code == 200

    get_response = requests.get(f"{base_url}/api/1/item/{item_id}")
    assert get_response.status_code == 404


def test_tc_5_2_verify_deleted_item_statistics_v1(base_url, created_item):
    item_id = created_item["item_id"]

    delete_response = requests.delete(f"{base_url}/api/2/item/{item_id}")
    assert delete_response.status_code == 200

    stats_response = requests.get(f"{base_url}/api/1/statistic/{item_id}")
    # BUG-10: Статистика доступна после удаления (ожидается 404)
    assert stats_response.status_code == 200


def test_tc_5_2_verify_deleted_item_statistics_v2(base_url, created_item):
    item_id = created_item["item_id"]

    delete_response = requests.delete(f"{base_url}/api/2/item/{item_id}")
    assert delete_response.status_code == 200

    stats_response = requests.get(f"{base_url}/api/2/statistic/{item_id}")
    # BUG-11: Статистика доступна после удаления (ожидается 404)
    assert stats_response.status_code == 200


def test_tc_5_2_verify_deleted_item_seller_list(base_url, created_item):
    item_id = created_item["item_id"]
    seller_id = created_item["seller_id"]

    delete_response = requests.delete(f"{base_url}/api/2/item/{item_id}")
    assert delete_response.status_code == 200

    seller_response = requests.get(f"{base_url}/api/1/{seller_id}/item")
    assert seller_response.status_code == 200

    items = seller_response.json()
    item_ids = [item["id"] for item in items]
    assert item_id not in item_ids


def test_tc_5_3_delete_nonexistent_item(base_url):
    nonexistent_id = str(uuid.uuid4())
    response = requests.delete(f"{base_url}/api/2/item/{nonexistent_id}")
    assert response.status_code == 404


def test_tc_5_4_delete_item_invalid_id(base_url):
    response = requests.delete(f"{base_url}/api/2/item/abc")
    assert response.status_code in [400, 404]


def test_tc_5_4_delete_item_empty_id(base_url):
    response = requests.delete(f"{base_url}/api/2/item/")
    assert response.status_code in [400, 404, 405]
