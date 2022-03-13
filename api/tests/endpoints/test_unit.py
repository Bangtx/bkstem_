from models.unit import Unit


def test_create_unit_name_none(client):
    """
    create unit with name none value
    :expected: return status code 422
    """
    response = client.post(
        "/units/",
        json={"name": None},
    )
    assert response.status_code == 422


def test_create_success_unit(client):
    """
    create unit success
    :expected: return unit data
    """
    response = client.post(
        "/units/",
        json={"name": "unit"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "unit"


def test_create_unit_ja_text(client):
    """
    create unit with japanese characters
    :expected: return unit data with full-width characters
    """
    response = client.post(
        "/units/",
        json={
            "name": "ﾃｨﾛ･ﾌｨﾅｰﾚ",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ティロ・フィナーレ"


def test_create_unit_duplicate(client):
    """
    create unit with duplicate name
    :expected: return status code 400
    """
    unit = {"name": "duplicate name"}

    client.post("/units/", json=unit)

    response = client.post("/units/", json=unit)
    assert response.status_code == 400


def test_update_unit_success(client):
    """
    update unit
    :expected: return status code 200 and data updated
    """
    response = client.post("/units/", json={"name": "unit name"})
    assert response.status_code == 200
    data = response.json()
    id = data["id"]

    response = client.put(
        f"/units/{id}",
        json={"name": "update unit name"},
    )
    assert response.status_code == 200
    data = response.json()
    data["id"] == id
    data["name"] == "update unit name"


def test_update_unit_exist_name(client):
    """
    update unit with name exist in other unit
    :expected: return status code 400
    """
    client.post("/units/", json={"name": "check exist name"})

    response = client.post("/units/", json={"name": "cname"})
    assert response.status_code == 200
    data = response.json()
    id = data["id"]

    response = client.put(f"/units/{id}", json={"name": "check exist name"})
    assert response.status_code == 400


def test_get_list_unit(client):
    """
    get list unit
    :expected: return status code 200 and array unit
    """
    response = client.post(
        "/units/",
        json={"name": "unit name 1"},
    )
    assert response.status_code == 200
    response = client.get("/units/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_show_unit_success(client, db):
    """
    get unit information
    :expected: return status code 200 and unit information
    """
    db.execute_sql(
        """
          INSERT INTO unit(id, name, yomi, created_at)
          VALUES (20, 'name test', 'yomi text', '2021-06-01');
        """
    )
    response = client.get("/units/20")
    assert response.status_code == 200
    assert {
        "id": 20,
        "name": "name test",
        "yomi": "yomi text",
        "search_str": None,
        "order_num": None,
        "created_at": "2021-06-01",
        "created_by": None,
        "active": True,
    } == response.json()


def test_show_unit_not_exist(client):
    """
    get unit not exist
    :expected: return status code 404
    """
    response = client.get(f"/units/2000")
    assert response.status_code == 404


def test_delete_unit_success(client, db):
    """
    delete a unit
    :expected: return status code 200 and unit.active is false
    """
    db.execute_sql(
        """
          INSERT INTO unit(id, name, created_at)
          VALUES (21, 'name1', '2021-06-01');
        """
    )
    response = client.delete("/units/21")
    assert response.status_code == 200
    unit = Unit.get_by_id(21)
    assert unit.active == False


def test_delete_unit_used_by_packing_result(client, db):
    """
    delete a unit used by packing result
    :expected: return status code 400
    """
    db.execute_sql(
        """
          INSERT INTO unit(id, name)
          VALUES (30, 'name');
          INSERT INTO packing_result(unit_id)
          VALUES (30);
        """
    )
    response = client.delete("/units/30")
    assert response.status_code == 400


def test_delete_unit_used_by_order_detail(client, db):
    """
    delete a unit used by order detail
    :expected: return status code 400
    """
    db.execute_sql(
        """
          INSERT INTO unit(id, name)
          VALUES (31, 'name');
          INSERT INTO order_detail(unit_id)
          VALUES (31);
        """
    )
    response = client.delete("/units/31")
    assert response.status_code == 400


def test_sort_unit(client, db):
    """
    sort unit
    :expected: return status code 200
    """
    db.execute_sql(
        """
          INSERT INTO unit(id, name, created_at, order_num)
          VALUES (201, 'name1', '2021-06-01', 201);
          VALUES (202, 'name1', '2021-06-01', 202);
        """
    )
    response = client.post(
        "/units/sort",
        json=[{"id": 201, "order_num": 10}, {"id": 202, "order_num": 20}],
    )
    assert response.status_code == 200
