import pytest
from models.variety import Variety

variety_enpoint = "/varieties/"
variety_data = {
    "name": None,
    "yomi": None,
    "name_eng": None,
    "short_name": "short name",
    "item": 1,
    "images": [],
}


@pytest.fixture(scope="module", autouse=True)
def fixtures_create_default_item(db):
    db.execute_sql(
        """
          DELETE FROM  item;
          INSERT INTO item(id, name, created_at)
          VALUES (1, 'item', '2021-06-03');
          INSERT INTO item(id, name, created_at)
          VALUES (2, 'item2', '2021-06-03');
        """
    )
    yield
    db.execute_sql(
        """
          DELETE FROM  item;
        """
    )


def test_create_variety_failed_name_none(client):
    """
    Create variety with name none value
    :expected: return status code 422
    """
    response = client.post(
        variety_enpoint,
        json=variety_data,
    )
    assert response.status_code == 422


def test_create_variety_success_with_unit(client):
    """
    Create variety success
    :expected: return 200 and variety data with item data
    """

    variety = variety_data
    variety["name"] = "variety"
    response = client.post(
        variety_enpoint,
        json=variety,
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    item = data["item"]
    assert item["id"] == 1
    assert item["name"] == "item"


def test_create_variety_success_with_ja_text(client):
    """
    Create variety with japanese characters
    :expected: return variety name with full-width characters
    """
    variety = variety_data
    variety["name"] = "ﾃｨﾛ･ﾌｨﾅｰﾚ"
    response = client.post(
        variety_enpoint,
        json=variety,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "ティロ・フィナーレ"


def test_create_variety_failed_duplicate_name(client):
    """
    Create itevarietym with duplicate name
    :expected: return status code 400
    """
    variety = variety_data
    variety["name"] = "variety"
    variety["item"] = 1
    response = client.post(
        variety_enpoint,
        json=variety,
    )
    assert response.status_code == 400


def test_create_variety_success_duplicate_name_in_another_item(client):
    """
    Create variety success
    :expected: return status code 200
    """

    variety = variety_data
    variety["name"] = "variety"
    variety["item"] = 2
    response = client.post(
        variety_enpoint,
        json=variety,
    )
    assert response.status_code == 200


def test_update_variety_success(client, db):
    """
    Update variety success
    :expected: return status code 200 and data update
    """

    db.execute_sql(
        """
          INSERT INTO variety(id, uuid, name, order_num, item_id, search_str)
          VALUES (10, 'edbc01b9-699d-4bdf-967d-3844d89479d2', 'variety name to update', 10, 1, 'search_str');
        """
    )
    variety = variety_data
    variety["name"] = "update name variety"
    variety["item"] = 1

    response = client.put(f"{variety_enpoint}10", json=variety)
    assert response.status_code == 200
    assert response.json()["name"] == variety["name"]
    assert "item" in response.json()
    assert "images" in response.json()


def test_update_variety_exist_name(client, db):
    """
    Update variety with name exist in other variety
    :expected: return status code 400
    """
    db.execute_sql(
        """
          INSERT INTO variety(id, name, order_num, item_id, search_str)
          VALUES (11, 'variety name exist', 11, 1, 'search_str');
        """
    )
    variety = variety_data
    variety["name"] = "variety name exist"
    variety["item"] = 1

    response = client.put(f"{variety_enpoint}10", json=variety)
    assert response.status_code == 400


def test_show_variety_success(client, db):
    """
    Get variety information
    :expected: return status code 200 and variety information
    """
    db.execute_sql(
        """
          INSERT INTO variety(id, name, yomi, order_num, item_id, search_str, created_at, uuid)
          VALUES (12, 'variety name exist', 'yomi text', 12, 1, 'search_str', '2021-06-03', 'f80c31ed-90ef-4af3-9cf0-9450faa3b4fb');
        """
    )
    response = client.get(f"{variety_enpoint}12")
    assert response.status_code == 200
    assert {
        "name": "variety name exist",
        "name_eng": None,
        "yomi": "yomi text",
        "short_name": None,
        "id": 12,
        "order_num": 12,
        "search_str": "search_str",
        "uuid": "f80c31ed-90ef-4af3-9cf0-9450faa3b4fb",
        "item": {"name": "item", "id": 1},
        "images": [],
        "active": True,
        "created_at": "2021-06-03",
        "created_by": None,
    } == response.json()


def test_show_variety_not_exist(client):
    """
    Get variety not exist
    :expected: return status code 404
    """
    response = client.get(f"{variety_enpoint}2000")
    assert response.status_code == 404


def test_delete_variety_success(client, db):
    """
    Delete variety
    :expected: return status code 200
    """
    db.execute_sql(
        """
          INSERT INTO variety(id, name, order_num, item_id, search_str, uuid)
          VALUES (13, 'variety name delete', 13, 1, 'search_str', 'f80c31ed-90ef-4af3-9cf0-9450faa3b4fb');
        """
    )
    response = client.delete(f"{variety_enpoint}13")
    assert response.status_code == 200
    variety = Variety.get_by_id(13)
    assert variety.active == False


def test_delete_variety_used_by_packing_result(client, db):
    """
    Delete variety used by packing result
    :expected: return status code 400
    """

    db.execute_sql(
        """
          INSERT INTO variety(id, name)
          VALUES (14, 'name');
          INSERT INTO packing_result(variety_id)
          VALUES (14);
        """
    )
    response = client.delete(f"{variety_enpoint}14")
    assert response.status_code == 400


def test_delete_variety_used_by_order_detail(client, db):
    """
    Delete variety used by order detail
    :expected: return status code 400
    """

    db.execute_sql(
        """
          INSERT INTO variety(id, name)
          VALUES (15, 'name');
          INSERT INTO order_detail(variety_id)
          VALUES (15);
        """
    )
    response = client.delete(f"{variety_enpoint}15")
    assert response.status_code == 400


def test_sort_variety_success(client, db):
    """
    Sort variety
    :expected: return status code 200
    """
    response = client.post(
        f"{variety_enpoint}sort",
        json=[{"id": 13, "order_num": 13}, {"id": 14, "order_num": 14}],
    )
    assert response.status_code == 200
