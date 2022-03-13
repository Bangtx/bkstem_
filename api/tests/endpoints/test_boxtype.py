from i18n import t
from models.boxtype import BoxType


def test_create_new_box_type_name_none(client):
    response = client.post(
        "/boxtype/",
        json={
            "name": None,
            "name_eng": "box type name english",
            "yomi": "yomi",
            "bundle_size": "bundle_size",
        },
    )
    assert response.status_code == 422


def test_create_new_box_type_yomi_none(client):
    response = client.post(
        "/boxtype/",
        json={
            "name": "name",
            "name_eng": "box type name english",
            "yomi": None,
            "bundle_size": "bundle size",
        },
    )
    assert response.status_code == 422


def test_create_new_box_type_no_bundle_size(client):
    response = client.post(
        "/boxtype/",
        json={
            "name": "name",
            "yomi": "yomi",
            "name_eng": "name eng",
            "bundle_size": None,
        },
    )
    assert response.status_code == 200


# def test_create_new_box_type_no_name_eng(client):
#     response = client.post(
#         '/boxtype/',
#         json={
#             'name': 'name_',
#             'yomi': 'yomi',
#             'name_eng': None,
#             'bundle_size': 'bundle size'
#         }
#     )
#     assert response.status_code == 200


# def test_update_sort(client):
#     '''
#     no order num -> F
#     '''
#     data = [
#         {
#             'name': 'name_',
#             'yomi': 'yomi',
#             'name_eng': 'name eng',
#             'bundle_size': 'bundle size',
#             'id': 24,
#             'order_num': None
#         }
#     ]
#     response = client.post(
#         '/boxtype/sort',
#         json=data
#     )
#     assert response.status_code == 422

#     # have order num

#     data[0]['order_num'] = 1
#     response = client.post(
#         '/boxtype/sort',
#         json=data
#     )
#     assert response.status_code == 200


# def test_update_box(client):
#     '''
#     no name and no yomi
#     '''
#     data_test = [
#         {
#             'name': None,
#             'yomi': 'string',
#             'name_eng': 'string',
#             'bundle_size': 'string'
#         },
#         {
#             'name': 'name',
#             'yomi': None,
#             'name_eng': 'string',
#             'bundle_size': 'string'
#         }
#     ]
#     for data in data_test:
#         response = client.put(
#             f'/boxtype/{1}',
#             json=data
#         )
#         assert response.status_code == 422

#     # no name eng and no bundle size

#     data = {
#         'name': 'teasst',
#         'yomi': 'string',
#         'name_eng': '',
#         'bundle_size': ''
#     }
#     response = client.put(
#         f'/boxtype/{24}',
#         json=data
#     )
#     assert response.status_code == 200


def test_delete_boxtype(client):
    response = client.delete(f"/boxtype/{1}")
    assert response.status_code == 200


def test_get_all_boxtype(client):
    response = client.get("/boxtype/")
    assert response.status_code == 200


# def test_get_one_box_type(client):
#     response = client.get(f'/boxtype/{2}')
#     assert response.status_code == 200
