from i18n import t
from models.quality import Quality


def test_create_quality_name_none(client):
    """
    create quality with name none value
    :expected: return status code 422
    """
    response = client.post(
        "/qualities/",
        json={
            "name": None,
            "name_eng": "quality name english",
            "short_name": "short name",
            "yomi": "yomi",
        },
    )
    assert response.status_code == 422


def test_create_success_quality(client):
    """
    create quality success
    :expected: return quality data
    """
    response = client.post(
        "/qualities/",
        json={
            "name": "quality name 1",
            "name_eng": None,
            "short_name": None,
            "yomi": None,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "quality name 1"


def test_create_quality_ja_text(client):
    """
    create quality with japanese characters
    :expected: return quality data with full-width characters
    """
    response = client.post(
        "/qualities/",
        json={
            "name": "ﾃｨﾛ･ﾌｨﾅｰﾚ",
            "name_eng": "quality name english",
            "short_name": "short name",
            "yomi": "yomi text",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ティロ・フィナーレ"
    assert data["name_eng"] == "quality name english"
    assert data["short_name"] == "short name"
    assert data["yomi"] == "yomi text"


def test_create_quality_duplicate(client):
    """
    create quality with duplicate name
    :expected: return status code 400
    """
    quality = {"name": "duplicate name"}

    client.post("/qualities/", json=quality)

    response = client.post("/qualities/", json=quality)
    assert response.status_code == 400
    assert response.json()["messages"] == [
        t("fmbiz.master.errors.duplicate_name")
    ]


def test_update_quality_success(client):
    """
    update quality
    :expected: return status code 200 and data updated
    """
    response = client.post(
        "/qualities/",
        json={
            "name": "quality name",
            "name_eng": "quality name english",
            "short_name": "short name",
            "yomi": "yomi text",
        },
    )
    assert response.status_code == 200
    data = response.json()
    size_id = data["id"]

    response = client.put(
        f"/qualities/{size_id}",
        json={
            "name": "update quality name",
            "name_eng": "update name english",
            "short_name": "update short name",
            "yomi": "update yomi",
        },
    )
    assert response.status_code == 200
    data = response.json()
    data["id"] == size_id
    data["name"] == "update quality name"


def test_update_quality_exist_name(client):
    """
    update quality with name exist in other quality
    :expected: return status code 400
    """
    client.post("/qualities/", json={"name": "check exist name"})

    response = client.post("/qualities/", json={"name": "name"})
    assert response.status_code == 200
    data = response.json()
    size_id = data["id"]

    response = client.put(
        f"/qualities/{size_id}", json={"name": "check exist name"}
    )
    assert response.status_code == 400
    assert response.json()["messages"] == [
        t("fmbiz.master.errors.duplicate_name")
    ]


def test_get_list_quality(client):
    """
    get list quality
    :expected: return status code 200 and array quality
    """
    response = client.post(
        "/qualities/",
        json={
            "name": "quality name",
            "name_eng": "quality name english",
            "short_name": "update short name",
            "yomi": "yomi text",
        },
    )
    assert response.status_code == 200
    response = client.get("/qualities/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_show_quality_success(client, db):
    """
    get quality information
    :expected: return status code 200 and quality information
    """
    db.execute_sql(
        """
          INSERT INTO quality(id, name, name_eng, short_name, yomi, created_at)
          VALUES (1000, 'name1', 'name english', 'short name', 'yomi text', '2021-05-25');
        """
    )
    response = client.get("/qualities/1000")
    assert response.status_code == 200
    assert {
        "id": 1000,
        "name": "name1",
        "name_eng": "name english",
        "short_name": "short name",
        "yomi": "yomi text",
        "search_str": None,
        "order_num": None,
        "created_at": "2021-05-25",
        "created_by": None,
        "active": True,
    } == response.json()


def test_show_quality_not_exist(client):
    """
    get quality not exist
    :expected: return status code 404
    """
    response = client.get(f"/qualities/2000")
    assert response.status_code == 404
    assert response.json()["messages"] == ["Quality not found"]


def test_delete_quality_success(client, db):
    """
    delete a quality
    :expected: return status code 200 and quality.active is false
    """
    db.execute_sql(
        """
          INSERT INTO quality(id, name, name_eng, short_name, yomi, created_at)
          VALUES (3000, 'name1', 'name english', 'short name', 'yomi text', '2021-05-25');
        """
    )
    response = client.delete("/qualities/3000")
    assert response.status_code == 200
    quality = Quality.get_by_id(3000)
    assert quality.active == False


def test_delete_quality_used_by_packing_result(client, db):
    """
    delete a quality used by packing result
    :expected: return status code 400
    """
    db.execute_sql(
        """
          INSERT INTO quality(id, name)
          VALUES (50, 'name');
          INSERT INTO packing_result(quality_id)
          VALUES (50);
        """
    )
    response = client.delete("/qualities/50")
    assert response.status_code == 400


def test_delete_quality_used_by_order_detail(client, db):
    """
    delete a quality used by order detail
    :expected: return status code 400
    """
    db.execute_sql(
        """
          INSERT INTO quality(id, name)
          VALUES (51, 'name');
          INSERT INTO order_detail(quality_id)
          VALUES (51);
        """
    )
    response = client.delete("/qualities/51")
    assert response.status_code == 400


def test_sort_quality(client, db):
    """
    sort quality
    :expected: return status code 200
    """
    db.execute_sql(
        """
          INSERT INTO quality(id, name, name_eng, short_name, yomi, created_at, order_num)
          VALUES (201, 'name1', 'name english', 'short name', 'yomi text', '2021-05-25', 201);
          VALUES (202, 'name1', 'name english', 'short name', 'yomi text', '2021-05-25', 202);
        """
    )
    response = client.post(
        "/qualities/sort",
        json=[{"id": 201, "order_num": 10}, {"id": 202, "order_num": 20}],
    )
    assert response.status_code == 200
