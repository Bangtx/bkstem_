import pytest
from models.item import Item

item_enpoint = "/items/"
item_data = {
    "name": None,
    "name_eng": "name english",
    "yomi": None,
    "short_name": "short name",
    "default_unit": 2,
    "images": [],
}


@pytest.fixture(scope="module", autouse=True)
def fixtures_create_default_unit(db):
    db.execute_sql(
        """
          DELETE FROM  unit;
          INSERT INTO unit(id, name, yomi, created_at)
          VALUES (2, 'unit', 'yomi text', '2021-06-03');
        """
    )
    yield
    db.execute_sql(
        """
          DELETE FROM  unit;
        """
    )


def test_create_item_failed_name_none(client):
    """
    create item with name none value
    :expected: return status code 422
    """
    response = client.post(
        item_enpoint,
        json=item_data,
    )
    assert response.status_code == 422


def test_create_item_success_with_unit(client):
    """
    Create item success
    :expected: return 200 and item data with unit data
    """

    item = item_data
    item["name"] = "item"
    response = client.post(
        item_enpoint,
        json=item,
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    unit = data["default_unit"]
    assert unit["id"] == 2
    assert unit["name"] == "unit"


def test_create_item_success_with_ja_text(client):
    """
    Create item with japanese characters
    :expected: return item name with full-width characters
    """
    item = item_data
    item["name"] = "ﾃｨﾛ･ﾌｨﾅｰﾚ"
    response = client.post(
        item_enpoint,
        json=item,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "ティロ・フィナーレ"


def test_create_item_failed_duplicate_name(client):
    """
    Create item with duplicate name
    :expected: return status code 400
    """
    item = item_data
    item["name"] = "item"
    response = client.post(
        item_enpoint,
        json=item,
    )
    assert response.status_code == 400


def test_update_item_success(client, db):
    """
    Update item success
    :expected: return status code 200 and data update
    """

    db.execute_sql(
        """
          INSERT INTO item(id, uuid, name, order_num, default_unit, search_str)
          VALUES (10, 'edbc01b9-699d-4bdf-967d-3844d89479d2', 'item name to update', 10, 2, 'search_str');
        """
    )
    item = item_data
    item["name"] = "update name item"

    response = client.put(f"{item_enpoint}10", json=item)
    assert response.status_code == 200
    assert response.json()["name"] == item["name"]
    assert "default_unit" in response.json()
    assert "images" in response.json()


def test_update_item_exist_name(client, db):
    """
    Update item with name exist in other item
    :expected: return status code 400
    """
    db.execute_sql(
        """
          INSERT INTO item(id, name, order_num, default_unit, search_str, uuid)
          VALUES (11, 'item name exist', 11, 2, 'search_str', 'f80c31ed-90ef-4af3-9cf0-9450faa3b4fb');
        """
    )
    item = item_data
    item["name"] = "item name exist"

    response = client.put(f"{item_enpoint}10", json=item)
    assert response.status_code == 400


def test_get_list_item_success(client):
    """
    Get list item
    :expected: return status code 200 and list item
    """
    response = client.get(item_enpoint)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_show_item_success(client, db):
    """
    Get item information
    :expected: return status code 200 and item information
    """
    db.execute_sql(
        """
          INSERT INTO item(id, name, yomi, order_num, default_unit, search_str, created_at, uuid, units)
          VALUES (12, 'item name exist', 'yomi text', 11, 2, 'search_str', '2021-06-03', 'f80c31ed-90ef-4af3-9cf0-9450faa3b4fb', '{2}');
        """
    )
    response = client.get(f"{item_enpoint}12")
    assert response.status_code == 200
    assert {
        "name": "item name exist",
        "name_eng": None,
        "yomi": "yomi text",
        "short_name": None,
        "id": 12,
        "order_num": 11,
        "search_str": "search_str",
        "uuid": "f80c31ed-90ef-4af3-9cf0-9450faa3b4fb",
        "default_unit": {"name": "unit", "id": 2},
        "units": [2],
        "images": [],
        "active": True,
        "created_at": "2021-06-03",
        "created_by": None,
    } == response.json()


def test_show_item_not_exist(client):
    """
    Get item not exist
    :expected: return status code 404
    """
    response = client.get(f"{item_enpoint}2000")
    assert response.status_code == 404


def test_delete_item_success(client, db):
    """
    Delete item
    :expected: return status code 200
    """
    db.execute_sql(
        """
          INSERT INTO item(id, name, order_num, default_unit, search_str, uuid)
          VALUES (13, 'item name delete', 11, 2, 'search_str', 'f80c31ed-90ef-4af3-9cf0-9450faa3b4fb');
        """
    )
    response = client.delete(f"{item_enpoint}13")
    assert response.status_code == 200
    item = Item.get_by_id(13)
    assert item.active == False


def test_delete_item_used_by_packing_result(client, db):
    """
    Delete item used by packing result
    :expected: return status code 400
    """

    db.execute_sql(
        """
          INSERT INTO item(id, name)
          VALUES (14, 'name');
          INSERT INTO packing_result(item_id)
          VALUES (14);
        """
    )
    response = client.delete(f"{item_enpoint}14")
    assert response.status_code == 400


def test_delete_item_used_by_order_detail(client, db):
    """
    Delete item used by order detail
    :expected: return status code 400
    """

    db.execute_sql(
        """
          INSERT INTO item(id, name)
          VALUES (15, 'name');
          INSERT INTO order_detail(item_id)
          VALUES (15);
        """
    )
    response = client.delete(f"{item_enpoint}15")
    assert response.status_code == 400


def test_sort_item_success(client, db):
    """
    Sort item
    :expected: return status code 200
    """
    response = client.post(
        f"{item_enpoint}sort",
        json=[{"id": 13, "order_num": 13}, {"id": 14, "order_num": 14}],
    )
    assert response.status_code == 200
