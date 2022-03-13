from i18n import t
from models.customer import Customer


def test_create_customer_name_none(client):
    """
    create customer with name none value
    :expected: return status code 422
    """
    response = client.post(
        "/customers/",
        json={
            "name": None,
            "yomi": "yomi",
            "short_name": "customer short name",
            "tel": "1234567",
            "email": "email",
            "fax": "fax",
            "code": "code",
        },
    )
    assert response.status_code == 422


def test_create_success_size(client):
    """
    create customer success
    :expected: return customer data
    """
    response = client.post(
        "/customers/",
        json={
            "name": "customer name 1",
            "yomi": None,
            "short_name": None,
            "tel": "1234567",
            "email": None,
            "fax": None,
            "code": None,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "customer name 1"
    assert data["tel"] == "1234567"


def test_create_customer_ja_text(client):
    """
    create customer with japanese characters
    :expected: return customer data with full-width characters
    """
    response = client.post(
        "/customers/",
        json={
            "name": "ﾃｨﾛ･ﾌｨﾅｰﾚ",
            "yomi": "yomi text",
            "tel": "123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ティロ・フィナーレ"
    assert data["tel"] == "123"
    assert data["yomi"] == "yomi text"


def test_create_customer_duplicate(client):
    """
    create customer with duplicate name
    :expected: return status code 400
    """
    customer = {
        "name": "duplicate name",
        "tel": "123",
    }

    client.post("/customers/", json=customer)

    response = client.post("/customers/", json=customer)
    assert response.status_code == 400
    assert response.json()["messages"] == [
        t("fmbiz.master.errors.duplicate_name")
    ]


def test_update_customer_success(client):
    """
    update customer
    :expected: return status code 200 and data updated
    """
    response = client.post(
        "/customers/",
        json={
            "name": "customer name 2",
            "yomi": "yomi text",
            "tel": "123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    customer_id = data["id"]

    response = client.put(
        f"/customers/{customer_id}",
        json={
            "name": "customer name 2 update",
            "yomi": "update yomi",
            "tel": "123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    data["id"] == customer_id
    data["name"] == "customer name 1 update"


def test_update_customer_exist_name(client):
    """
    update size with name exist in other size
    :expected: return status code 400
    """
    client.post("/customers/", json={"name": "check exist name", "tel": "123"})

    response = client.post("/customers/", json={"name": "cname", "tel": "ctel"})
    assert response.status_code == 200
    data = response.json()
    customer_id = data["id"]

    response = client.put(
        f"/customers/{customer_id}",
        json={"name": "check exist name", "tel": "123"},
    )
    assert response.status_code == 400
    assert response.json()["messages"] == [
        t("fmbiz.master.errors.duplicate_name")
    ]


def test_get_list_size(client):
    """
    get list customer
    :expected: return status code 200 and array customer
    """
    response = client.post(
        "/customers/",
        json={"name": "customer name", "tel": "123"},
    )
    assert response.status_code == 200
    response = client.get("/customers/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_show_customer_success(client, db):
    """
    get customer information
    :expected: return status code 200 and customer information
    """
    db.execute_sql(
        """
          INSERT INTO customer(id, name, yomi, tel, fax, email, code, created_at)
          VALUES (1000, 'name',  'yomi', '123', '123', '123', '123', '2021-05-25');
        """
    )
    response = client.get("/customers/1000")
    assert response.status_code == 200
    assert {
        "id": 1000,
        "name": "name",
        "yomi": "yomi",
        "tel": "123",
        "fax": "123",
        "email": "123",
        "code": "123",
        "short_name": None,
        "search_str": None,
        "order_num": None,
        "created_at": "2021-05-25",
        "created_by": None,
        "active": True,
    } == response.json()


def test_show_customer_not_exist(client):
    """
    get customer not exist
    :expected: return status code 404
    """
    response = client.get(f"/customers/2000")
    assert response.status_code == 404
    assert response.json()["messages"] == ["Customer not found"]


def test_delete_customer_success(client, db):
    """
    delete a customer
    :expected: return status code 200 and customer.active is false
    """
    db.execute_sql(
        """
          INSERT INTO customer(id, name, yomi, tel, fax, email, code, created_at)
          VALUES (3000, 'name1', 'yomi', '123', '123', '123', '123', '2021-05-25');
        """
    )
    response = client.delete("/customers/3000")
    assert response.status_code == 200
    response = client.get("/customers/3000")
    customer = Customer.get_by_id(3000)
    assert customer.active == False


def test_delete_customer_used_by_packing_result(client, db):
    """
    delete a customer used by packing result
    :expected: return status code 400
    """
    db.execute_sql(
        """
          INSERT INTO customer(id, name)
          VALUES (51, 'name');
          INSERT INTO public."order"(customer_id)
          VALUES (51);
        """
    )
    response = client.delete("/customers/51")
    assert response.status_code == 400


def test_sort_size(client, db):
    """
    sort customer
    :expected: return status code 200
    """
    db.execute_sql(
        """
          INSERT INTO customer(id, name, tel, fax, email, code, created_at, order_num)
          VALUES (201, 'name1', '123', '123', '123', '123', '2021-05-25', 201);
          VALUES (202, 'name1', '123', '123', '123', '123', '2021-05-25', 202);
        """
    )
    response = client.post(
        "/customers/sort",
        json=[{"id": 201, "order_num": 10}, {"id": 202, "order_num": 20}],
    )
    assert response.status_code == 200
