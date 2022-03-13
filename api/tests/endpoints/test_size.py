from i18n import t
from models.size import Size


def test_create_size_name_none(client):
    """
    create size with name none value
    :expected: return status code 422
    """
    response = client.post(
        "/sizes/",
        json={"name": None, "name_eng": "size name english", "yomi": "yomi"},
    )
    assert response.status_code == 422


def test_create_success_size(client):
    """
    create size success
    :expected: return size data
    """
    response = client.post(
        "/sizes/",
        json={"name": "size name 1", "name_eng": None, "yomi": None},
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "size name 1"


def test_create_size_ja_text(client):
    """
    create size with japanese characters
    :expected: return size data with full-width characters
    """
    response = client.post(
        "/sizes/",
        json={
            "name": "ﾃｨﾛ･ﾌｨﾅｰﾚ",
            "name_eng": "size name english",
            "yomi": "yomi text",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ティロ・フィナーレ"
    assert data["name_eng"] == "size name english"
    assert data["yomi"] == "yomi text"


def test_create_size_duplicate(client):
    """
    create size with duplicate name
    :expected: return status code 400
    """
    size = {"name": "duplicate name"}

    client.post("/sizes/", json=size)

    response = client.post("/sizes/", json=size)
    assert response.status_code == 400
    assert response.json()["messages"] == [
        t("fmbiz.master.errors.duplicate_name")
    ]


def test_update_size_success(client):
    """
    update size
    :expected: return status code 200 and data updated
    """
    response = client.post(
        "/sizes/",
        json={
            "name": "size name",
            "name_eng": "size name english",
            "yomi": "yomi text",
        },
    )
    assert response.status_code == 200
    data = response.json()
    size_id = data["id"]

    response = client.put(
        f"/sizes/{size_id}",
        json={
            "name": "update size name",
            "name_eng": "update name english",
            "yomi": "update yomi",
        },
    )
    assert response.status_code == 200
    data = response.json()
    data["id"] == size_id
    data["name"] == "update size name"


def test_update_size_exist_name(client):
    """
    update size with name exist in other size
    :expected: return status code 400
    """
    client.post("/sizes/", json={"name": "check exist name"})

    response = client.post("/sizes/", json={"name": "cname"})
    assert response.status_code == 200
    data = response.json()
    size_id = data["id"]

    response = client.put(
        f"/sizes/{size_id}", json={"name": "check exist name"}
    )
    assert response.status_code == 400
    assert response.json()["messages"] == [
        t("fmbiz.master.errors.duplicate_name")
    ]


def test_get_list_size(client):
    """
    get list size
    :expected: return status code 200 and array size
    """
    response = client.post(
        "/sizes/",
        json={
            "name": "size name",
            "name_eng": "size name english",
            "yomi": "yomi text",
        },
    )
    assert response.status_code == 200
    response = client.get("/sizes/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_show_size_success(client, db):
    """
    get size information
    :expected: return status code 200 and size information
    """
    db.execute_sql(
        """
          INSERT INTO size(id, name, name_eng, yomi, created_at)
          VALUES (1000, 'name1', 'name english', 'yomi text', '2021-05-25');
        """
    )
    response = client.get("/sizes/1000")
    assert response.status_code == 200
    assert {
        "id": 1000,
        "name": "name1",
        "name_eng": "name english",
        "yomi": "yomi text",
        "search_str": None,
        "order_num": None,
        "created_at": "2021-05-25",
        "created_by": None,
        "active": True,
    } == response.json()


def test_show_size_not_exist(client):
    """
    get size not exist
    :expected: return status code 404
    """
    response = client.get(f"/sizes/2000")
    assert response.status_code == 404
    assert response.json()["messages"] == ["Size not found"]


def test_delete_size_success(client, db):
    """
    delete a size
    :expected: return status code 200 and size.active is false
    """
    db.execute_sql(
        """
          INSERT INTO size(id, name, name_eng, yomi, created_at)
          VALUES (3000, 'name1', 'name english', 'yomi text', '2021-05-25');
        """
    )
    response = client.delete("/sizes/3000")
    assert response.status_code == 200
    size = Size.get_by_id(3000)
    assert size.active == False


def test_delete_size_used_by_packing_result(client, db):
    """
    delete a size used by packing result
    :expected: return status code 400
    """
    db.execute_sql(
        """
          INSERT INTO size(id, name)
          VALUES (50, 'name');
          INSERT INTO packing_result(size_id)
          VALUES (50);
        """
    )
    response = client.delete("/sizes/50")
    assert response.status_code == 400


def test_delete_size_used_by_order_detail(client, db):
    """
    delete a size used by order detail
    :expected: return status code 400
    """
    db.execute_sql(
        """
          INSERT INTO size(id, name)
          VALUES (51, 'name');
          INSERT INTO order_detail(size_id)
          VALUES (51);
        """
    )
    response = client.delete("/sizes/51")
    assert response.status_code == 400


def test_sort_size(client, db):
    """
    sort size
    :expected: return status code 200
    """
    db.execute_sql(
        """
          INSERT INTO size(id, name, name_eng, yomi, created_at, order_num)
          VALUES (201, 'name1', 'name english', 'yomi text', '2021-05-25', 201);
          VALUES (202, 'name1', 'name english', 'yomi text', '2021-05-25', 202);
        """
    )
    response = client.post(
        "/sizes/sort",
        json=[{"id": 201, "order_num": 10}, {"id": 202, "order_num": 20}],
    )
    assert response.status_code == 200
