import pytest
from models.packing_result import PackingResult

enpoint = "/packing_results/"


@pytest.fixture(scope="module", autouse=True)
def fixtures_default_data(db):
    db.execute_sql(
        """
          DELETE FROM  packing_result;

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

          DELETE FROM  color;
          INSERT INTO color(id, name, code)
          VALUES (1, 'white', '#f9f9eb'), (2, 'black', '#000000');

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
          DELETE FROM  color;
        """
    )


def test_create_packing_result_failed_invalid_value(client):
    """
    Create packing result with invalid value
    :expected: return status code 422
    """

    packing_result = {
        "boxes": None,
        "item_id": None,
        "variety_id": None,
    }
    response = client.post(enpoint, json=packing_result)
    assert response.status_code == 422

    packing_result["boxes"] = 10
    response = client.post(enpoint, json=packing_result)
    assert response.status_code == 422

    packing_result["item_id"] = 1
    response = client.post(enpoint, json=packing_result)
    assert response.status_code == 422


# def test_create_packing_result_success(client):
#     """
#     Create packing result success
#     :expected: return packing result data
#     """
#     packing_result = {
#         "auction_date": "2020-06-29",
#         "quantity": 20,
#         "boxes": 20,
#         "item_id": 1,
#         "box_type_id": 7,
#         "size_id": 1,
#         "variety_id": 2,
#         "quality_id": 1,
#         "color_id": 2,
#         "unit_id": 1,
#         "total_stems": 22,
#     }
#     response = client.post(f"{enpoint}", json=packing_result)
#     assert response.status_code == 200
#     data = response.json()

#     assert "size" in data
#     assert "color" in data
#     assert "unit" in data
#     assert "quality" in data
#     assert data["quantity"] == 20
#     assert data["boxes"] == 20
#     assert data["total_stems"] == 22
#     assert data["box_type_id"] == 7
#     assert data["auction_date"] == "2020-06-29"
#     assert data["item"] == {"id": 1, "name": "item name"}
#     assert data["variety"] == {"id": 2, "name": "variety name 2"}


# def test_update_packing_result_success(client, db):
#     """
#     Update packing result
#     :expected: return status code 200 and data updated
#     """
#     db.execute_sql(
#         """
#           INSERT INTO packing_result(
#               id,
#               auction_date,
#               item_id,
#               variety_id,
#               size_id,
#               color_id,
#               quality_id,
#               box_type_id,
#               unit_id,
#               total_stems,
#               boxes,
#               quantity
#             )
#           VALUES (
#               11,
#               '2020-06-30',
#               1,
#               1,
#               1,
#               2,
#               1,
#               7,
#               1,
#               22,
#               20,
#               20
#               );
#         """
#     )
#     packing_result = {
#         "auction_date": "2020-06-30",
#         "quantity": 20,
#         "boxes": 20,
#         "item_id": 1,
#         "box_type_id": 7,
#         "size_id": 1,
#         "variety_id": 2,
#         "quality_id": 1,
#         "color_id": 2,
#         "unit_id": 1,
#         "total_stems": 222,
#     }
#     response = client.put(f"{enpoint}11", json=packing_result)
#     assert response.status_code == 200
#     data = response.json()
#     assert "size" in data
#     assert "color" in data
#     assert "unit" in data
#     assert "quality" in data
#     assert data["quantity"] == 20
#     assert data["boxes"] == 20
#     assert data["total_stems"] == 222
#     assert data["box_type_id"] == 7
#     assert data["auction_date"] == "2020-06-30"
#     assert data["item"] == {"id": 1, "name": "item name"}
#     assert data["variety"] == {"id": 2, "name": "variety name 2"}


# def test_get_list_packing_result(client):
#     """
#     Get list packing result
#     :expected: return status code 200 and list packing result
#     """
#     response = client.get(enpoint)
#     assert len(response.json()) > 0


# def test_get_packing_result_summary_from_date(client):
#     """
#     Get list packing result
#     :expected: return status code 200 and list packing result
#     """
#     response = client.get(
#         f"{enpoint}get_packing_result_summary?start_date=2020-06-29"
#     )
#     assert len(response.json()) == 2


# def test_get_packing_result_summary_in_range(client):
#     """
#     Get list packing result
#     :expected: return status code 200 and list packing result
#     """
#     start_date = "start_date=2020-06-29"
#     end_date = "end_date=2020-06-30"

#     response = client.get(
#         f"{enpoint}get_packing_result_summary?{start_date}&{end_date}"
#     )
#     assert len(response.json()) == 2


# def test_get_packing_result_summary_in_one_day(client, db):
#     """
#     Get list packing result
#     :expected: return status code 200 and list packing result
#     """
#     db.execute_sql(
#         """
#           INSERT INTO packing_result(
#               auction_date,
#               item_id,
#               variety_id,
#               size_id,
#               color_id,
#               quality_id,
#               box_type_id,
#               unit_id,
#               total_stems,
#               boxes,
#               quantity
#             )
#           VALUES (
#               '2020-06-29',
#               1,
#               1,
#               1,
#               2,
#               1,
#               7,
#               1,
#               22,
#               20,
#               20
#               );
#         """
#     )
#     start_date = "start_date=2020-06-29"
#     end_date = "end_date=2020-06-29"

#     response = client.get(
#         f"{enpoint}get_packing_result_summary?{start_date}&{end_date}"
#     )

#     assert response.status_code == 200
#     assert len(response.json()) == 1
#     data = response.json()
#     assert data[0]["boxes"] == 40
#     assert data[0]["total_stems"] == 44


# def test_get_packing_result_by_date(client):
#     """
#     Create packing result success
#     :expected: return packing result data
#     """
#     response = client.get(
#         f"{enpoint}get_packing_result_by_date?date=2020-06-29"
#     )
#     assert response.status_code == 200
#     assert len(response.json()) == 2


def test_show_packing_result_not_exist(client):
    """
    get packing result not exist
    :expected: return status code 404
    """
    response = client.get(f"{enpoint}2000")
    assert response.status_code == 404


def test_delete_packing_result_success(client, db):
    """
    Delete a packing result
    :expected: return status code 200
    """
    db.execute_sql(
        """
          INSERT INTO packing_result(
              id,
              auction_date,
              item_id,
              variety_id,
              size_id,
              color_id,
              quality_id,
              box_type_id,
              unit_id,
              total_stems,
              boxes,
              quantity
            )
          VALUES (
              111,
              '2020-06-30',
              1,
              1,
              1,
              2,
              1,
              7,
              1,
              22,
              20,
              20
              );
        """
    )
    response = client.delete(f"{enpoint}111")
    assert response.status_code == 200
    packing_result = PackingResult.get_by_id(111)
    assert packing_result.active == False


def test_delete_packing_result_failed(client):
    """
    Delete packing_result not exist
    :expected: return status code 404
    """
    response = client.delete(f"{enpoint}200")
    assert response.status_code == 404
