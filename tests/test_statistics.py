import uuid
import requests


def test_tc_4_1_get_statistics_v1(base_url, created_item):
    item_id = created_item["item_id"]
    expected_stats = created_item["payload"]["statistics"]

    response = requests.get(f"{base_url}/api/1/statistic/{item_id}")
    assert response.status_code == 200

    stats_list = response.json()
    assert isinstance(stats_list, list)
    assert len(stats_list) == 1

    stats = stats_list[0]
    assert "likes" in stats
    assert "viewCount" in stats
    assert "contacts" in stats

    assert isinstance(stats["likes"], int)
    assert isinstance(stats["viewCount"], int)
    assert isinstance(stats["contacts"], int)

    assert stats["likes"] == expected_stats["likes"]
    assert stats["viewCount"] == expected_stats["viewCount"]
    assert stats["contacts"] == expected_stats["contacts"]


def test_tc_4_2_get_statistics_v2(base_url, created_item):
    item_id = created_item["item_id"]
    expected_stats = created_item["payload"]["statistics"]

    response = requests.get(f"{base_url}/api/2/statistic/{item_id}")
    assert response.status_code == 200

    stats_list = response.json()
    assert isinstance(stats_list, list)
    assert len(stats_list) == 1

    stats = stats_list[0]
    assert stats["likes"] == expected_stats["likes"]
    assert stats["viewCount"] == expected_stats["viewCount"]
    assert stats["contacts"] == expected_stats["contacts"]

    response_v1 = requests.get(f"{base_url}/api/1/statistic/{item_id}")
    stats_v1 = response_v1.json()[0]
    assert stats == stats_v1


def test_tc_4_3_get_statistics_nonexistent_item(base_url):
    nonexistent_id = str(uuid.uuid4())

    response_v1 = requests.get(f"{base_url}/api/1/statistic/{nonexistent_id}")
    assert response_v1.status_code == 404

    response_v2 = requests.get(f"{base_url}/api/2/statistic/{nonexistent_id}")
    assert response_v2.status_code == 404


def test_tc_4_4_get_statistics_invalid_id_v1(base_url):
    response = requests.get(f"{base_url}/api/1/statistic/abc")
    assert response.status_code in [400, 404]


def test_tc_4_4_get_statistics_invalid_id_v2(base_url):
    response = requests.get(f"{base_url}/api/2/statistic/abc")
    assert response.status_code in [400, 404]


def test_tc_4_4_get_statistics_empty_id_v1(base_url):
    response = requests.get(f"{base_url}/api/1/statistic/")
    assert response.status_code in [400, 404]


def test_tc_4_4_get_statistics_empty_id_v2(base_url):
    response = requests.get(f"{base_url}/api/2/statistic/")
    assert response.status_code in [400, 404]
