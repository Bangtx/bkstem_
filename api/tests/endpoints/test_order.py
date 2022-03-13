import pytest
from models.order import Order
from models.order_detail import OrderDetail

order_enpoint = "/orders/"


@pytest.fixture(scope="module", autouse=True)
def fixture_customer(db):
    db.execute_sql(
        """
          DELETE FROM  customer;
          INSERT INTO customer(id, name, short_name, tel, fax, search_str)
          VALUES (1, 'customer', 'short name', '0123456789', 'fax', 'customer'),
          (2, 'customer 2', 'short name 2', '0123456789', 'fax', 'customer 2');

          DELETE FROM  item;
          INSERT INTO item(id, name)
          VALUES (1, 'item name');

          DELETE FROM  variety;
          INSERT INTO variety(id, name)
          VALUES (2, 'variety name 2');

          DELETE FROM order_detail;
          INSERT INTO order_detail(id, order_id, quantity, boxes, item_id, variety_id)
          VALUES (1, 20, 5, 200, 1, 2), (2, 20, 5, 200, 1, 2);
        """
    )
    yield
    db.execute_sql(
        """
          DELETE FROM  customer;
          DELETE FROM  item;
          DELETE FROM  variety;
          DELETE FROM order_detail;
        """
    )


def test_create_order_failed_auction_date_none(client):
    """
    Create order with auction date none value
    :expectee: return status code 422
    """
    order = {"auction_date": None, "customer_id": 1}

    response = client.post(
        order_enpoint,
        json=order,
    )
    assert response.status_code == 422


def test_create_order_failed_auction_date_invalid(client):
    """
    Create order with auction date invalid value
    :expectee: return status code 422
    """
    order = {"auction_date": "12/34/56", "customer_id": 1}

    response = client.post(
        order_enpoint,
        json=order,
    )
    assert response.status_code == 422


def test_create_order_failed_customer_invalid(client):
    """
    Create order with customer invalid value
    :expectee: return status code 422
    """
    order = {"auction_date": "2021-06-24", "customer_id": None}

    response = client.post(
        order_enpoint,
        json=order,
    )
    assert response.status_code == 422


def test_create_order_success(client):
    """
    Create order success
    :expectee: return status code 200
    """
    order = {"auction_date": "2021-06-24", "customer_id": 1}

    response = client.post(
        order_enpoint,
        json=order,
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["customer"]["name"] == "customer"
    assert response.json()["auction_date"] == "2021-06-24"


def test_update_order_failed_invalid_value(client, db):
    """
    Update order with invalid value
    :expectee: return status code 422
    """
    order = {"auction_date": "2021-06-24", "customer_id": None}

    response = client.put(
        f"{order_enpoint}1",
        json=order,
    )
    assert response.status_code == 422

    order = {"auction_date": None, "customer_id": 1}
    response = client.put(
        f"{order_enpoint}1",
        json=order,
    )
    assert response.status_code == 422


def test_update_order_success(client, db):
    """
    Update order success
    : expectee: return status code 200
    """
    order = {"auction_date": "2021-07-24", "customer_id": 1}
    response = client.put(
        f"{order_enpoint}1",
        json=order,
    )
    assert response.status_code == 200


def test_show_order_not_exist(client):
    """
    Get order not exist
    :expected: return status code 404
    """
    response = client.get(f"{order_enpoint}2000")
    assert response.status_code == 404


def test_show_order_success(client):
    """
    Get order information
    :expected: return status code 200 and order information
    """
    response = client.get(f"{order_enpoint}1")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "auction_date" in response.json()
    assert response.json()["customer"]["name"] == "customer"


def test_list_order_and_filter_success(client, db):
    """
    Get list order information
    :expected: return status code 200 and order list information
    """
    db.execute_sql(
        """
          INSERT INTO "order"(auction_date, customer_id)
          VALUES ('2021-07-24', 1), 
          ('2021-07-24', 2), ('2021-07-25', 2);
        """
    )
    response = client.get(order_enpoint)
    assert response.status_code == 200
    assert len(response.json()) > 0

    response = client.get(f"{order_enpoint}?auction_date=2021-07-24")
    assert len(response.json()) == 3

    response = client.get(f"{order_enpoint}?customer_id=2")
    assert len(response.json()) == 2

    response = client.get(
        f"{order_enpoint}?auction_date=2021-07-24&customer_id=2"
    )
    assert len(response.json()) == 1


def test_delete_order_success(client, db):
    """
    Delete order
    :expected: return status code 200
    """
    db.execute_sql(
        """
          INSERT INTO "order"(id, auction_date, customer_id)
          VALUES (20, '2021-07-24', 2);
        """
    )

    response = client.delete(f"{order_enpoint}20")
    assert response.status_code == 200
    order = Order.get_by_id(20)
    assert order.active == False

    details = OrderDetail.select().where(
        OrderDetail.id.in_([1, 2])
    )  # pylint: disable=no-member
    for detail in details:
        assert detail.active == False


def test_delete_order_failed(client):
    """
    Delete order not exist
    :expected: return status code 404
    """
    response = client.delete(f"{order_enpoint}200")
    assert response.status_code == 404


def test_get_order_summary_information(client, db):
    """
    Get order group by auction date and customer id
    :expected: return status code 200
    """
    db.execute_sql(
        """
          DELETE FROM "order";
          INSERT INTO "order"(id, auction_date, customer_id)
          VALUES (1, '2021-07-24', 1), (2, '2021-06-24', 2);

          DELETE FROM order_detail;
          INSERT INTO order_detail(id, order_id, quantity, boxes, item_id, variety_id)
          VALUES (1, 1, 5, 200, 1, 2), (2, 1, 5, 1, 1, 2), (3, 2, 5, 1, 1, 2), (4, 2, 5, 1, 1, 2);
        """
    )
    response = client.get(f"{order_enpoint}summary?by=date")
    assert response.status_code == 200
    data = response.json()
    data == [
        {
            "auction_date": "2021-07-24",
            "total_boxes": 10,
            "total_stems": 0,
            "assign_boxes": 0,
            "assign_stems": 0,
        },
        {
            "auction_date": "2021-06-24",
            "total_boxes": 10,
            "total_stems": 0,
            "assign_boxes": 0,
            "assign_stems": 0,
        },
    ]

    response = client.get(f"{order_enpoint}summary?by=customer")
    assert response.status_code == 200
    data = response.json()
    data == [
        {
            "customer": {"id": 1, "name": "customer", "search_str": "customer"},
            "total_boxes": 10,
            "total_stems": 0,
            "assign_boxes": 0,
            "assign_stems": 0,
            "ids": [1],
        },
        {
            "customer": {
                "id": 2,
                "name": "customer 2",
                "search_str": "customer 2",
            },
            "total_boxes": 10,
            "total_stems": 0,
            "assign_boxes": 0,
            "assign_stems": 0,
            "ids": [2],
        },
    ]

    response = client.get(
        f"{order_enpoint}summary?by=customer&auction_date=2021-07-24"
    )
    assert response.status_code == 200
    data = response.json()
    data == [
        {
            "customer": {"id": 1, "name": "customer", "search_str": "customer"},
            "total_boxes": 10,
            "total_stems": 0,
            "assign_boxes": 0,
            "assign_stems": 0,
            "ids": [1, 2],
        }
    ]
    db.execute_sql(
        """
          DELETE FROM "order";
          DELETE FROM order_detail;
        """
    )
