import pytest
from models.order_detail import OrderDetail

enpoint = "/order_details/"


@pytest.fixture(scope="module", autouse=True)
def fixtures_default_data(db):
    db.execute_sql(
        """
          DELETE FROM  unit;
          INSERT INTO unit(id, name, yomi)
          VALUES (1, 'unit', 'yomi text');

          DELETE FROM  item;
          INSERT INTO item(id, uuid, name, order_num, default_unit, search_str)
          VALUES (1, 'edbc01b9-699d-4bdf-967d-3844d89479d2',
                  'item name', 1, 1, 'search_str');

          DELETE FROM  variety;
          INSERT INTO variety(id, name, order_num, item_id, search_str)
          VALUES (1, 'variety name 1', 1, 1, 'search_str'),
                 (2, 'variety name 2', 1, 1, 'search_str');

          DELETE FROM  size;
          INSERT INTO size(id, name)
          VALUES (1, 'size');

          DELETE FROM  quality;
          INSERT INTO quality(id, name)
          VALUES (1, 'quality');

          DELETE FROM  order_type;
          INSERT INTO order_type(id, name)
          VALUES (1, 'fm'),  (2, 'seri');

          DELETE FROM  color;
          INSERT INTO color(id, name, code)
          VALUES (1, 'white', '#f9f9eb'), (2, 'black', '#000000');

          DELETE FROM  "order";
          INSERT INTO "order"(id, auction_date, customer_id, created_at)
          VALUES (10, '2021-07-24', 1, '2021-07-24');

          DELETE FROM  customer;
          INSERT INTO customer(id, name, search_str)
          VALUES (1, 'customer', 'customer');
        """
    )
    yield
    db.execute_sql(
        """
          DELETE FROM  item;
          DELETE FROM  unit;
          DELETE FROM  variety;
          DELETE FROM  quality;
          DELETE FROM  size;
          DELETE FROM  order_type;
          DELETE FROM  color;
          DELETE FROM  "order";
          DELETE FROM  customer;
        """
    )


def test_create_order_detail_failed_invalid_value(client):
    """
    Create order detail with invalid value
    :expected: return status code 422
    """

    order_detail = {
        "boxes": None,
        "item_id": None,
        "variety_id": None,
        "order_id": 1,
    }
    response = client.post(enpoint, json=order_detail)
    assert response.status_code == 422

    order_detail["boxes"] = 10
    response = client.post(enpoint, json=order_detail)
    assert response.status_code == 422

    order_detail["item_id"] = 1
    response = client.post(enpoint, json=order_detail)
    assert response.status_code == 422


def test_create_order_detail_success(client):
    """
    Create order detail success
    :expected: return order detail data
    """
    order_detail = {"boxes": 20, "item_id": 1, "variety_id": 2, "order_id": 10}
    response = client.post(enpoint, json=order_detail)
    assert response.status_code == 200
    data = response.json()

    assert "order" in data
    assert "size" in data
    assert "colors" in data
    assert "quality" in data
    assert "unit" in data
    assert "order_type" in data
    assert data["boxes"] == 20
    assert data["item"] == {"id": 1, "name": "item name"}
    assert data["variety"] == {"id": 2, "name": "variety name 2"}


def test_update_order_detail_succsess(client, db):
    """
    Update order detail
    :expected: return status code 200 and data updated
    """
    db.execute_sql(
        """
          INSERT INTO order_detail(id, order_id, quantity, boxes)
          VALUES (10, 10, 5, 200);
        """
    )
    order_detail = {
        "quantity": 5,
        "boxes": 200,
        "item_id": 1,
        "variety_id": 2,
        "order_id": 10,
        "color_ids": [1, 2],
        "quality_id": 1,
        "size_id": 1,
        "order_type_id": 1,
    }
    response = client.put(f"{enpoint}10", json=order_detail)
    assert response.status_code == 200
    data = response.json()
    assert data["boxes"] == 200
    assert data["quantity"] == 5
    assert data["quality"]["name"] == "quality"
    assert data["order_type"]["name"] == "fm"
    assert len(data["color_ids"]) == 2


def test_get_list_order_detail(client):
    """
    Get list order detail
    :expected: return status code 200 and list order detail
    """
    response = client.get(enpoint)
    assert len(response.json()) > 0
    response = client.get(f"{enpoint}?order_id=10")
    assert len(response.json()) == 2
    response = client.get(f"{enpoint}?order_id=2")
    assert len(response.json()) == 0
    response = client.get(f"{enpoint}?variety_id=1")
    assert len(response.json()) == 0
    response = client.get(f"{enpoint}?variety_id=2")
    assert len(response.json()) == 2
    response = client.get(f"{enpoint}?auction_date=2021-07-24")
    assert len(response.json()) == 2


def test_show_order_detail_success(client, db):
    """
    Get order detail information
    :expected: return status code 200 and detail information
    """
    db.execute_sql(
        """
          INSERT INTO order_detail(id, order_id, quantity, boxes, price, item_id, variety_id, size_id, color_ids, quality_id, unit_id, order_type_id, created_at)
          VALUES (11, 10, 5, 200, 10, 1, 2, 1, '{1,2}', 1, 1, 1, '2021-07-24');
        """
    )
    response = client.get(f"{enpoint}11")
    data = response.json()

    assert data == {
        "is_lock": False,
        "quantity": 5,
        "boxes": 200,
        "price": 10,
        "stems": None,
        "remark": None,
        "buyer_info": None,
        "id": 11,
        "item": {"id": 1, "name": "item name"},
        "variety": {"id": 2, "name": "variety name 2"},
        "size": {"id": 1, "name": "size"},
        "colors": [
            {"code": "#f9f9eb", "id": 1, "name": "white"},
            {"code": "#000000", "id": 2, "name": "black"},
        ],
        "color_ids": [1, 2],
        "quality": {"id": 1, "name": "quality"},
        "unit": {"id": 1, "name": "unit"},
        "order_type": {"id": 1, "name": "fm"},
        "order": {
            "auction_date": "2021-07-24",
            "id": 10,
            "customer": {
                "id": 1,
                "name": "customer",
                "code": None,
            },
        },
        "is_special": False,
        "is_assigned": False,
    }


def test_show_order_detail_not_exist(client):
    """
    get order detail not exist
    :expected: return status code 404
    """
    response = client.get(f"{enpoint}2000")
    assert response.status_code == 404


def test_delete_order_detail_success(client, db):
    """
    Delete a order detail
    :expected: return status code 200
    """
    db.execute_sql(
        """
          INSERT INTO order_detail(id, order_id, quantity, boxes, item_id, variety_id)
          VALUES (20, 1, 5, 200, 1, 2);
        """
    )
    response = client.delete(f"{enpoint}20")
    assert response.status_code == 200
    detail = OrderDetail.get_by_id(20)
    assert detail.active == False


def test_delete_order_detail_failed(client):
    """
    Delete order detail not exist
    :expected: return status code 404
    """
    response = client.delete(f"{enpoint}200")
    assert response.status_code == 404
