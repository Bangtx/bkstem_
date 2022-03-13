def test_get_pronunciation_failed_missing_value(client):
    """
    call API without input value
    :expected: return status code 422
    """
    response = client.get("/common/get-pronunciation")
    assert response.status_code == 422


def test_get_pronunciation_success_status_code(client):
    """
    call API normally to check status code
    :expected: return status code 200
    """
    response = client.get("/common/get-pronunciation?text=qwerty")
    assert response.status_code == 200


def test_get_pronunciation_success_return_value(client):
    """
    call API with a string which include full-width alphabet character, kanji,
    katakana, hiragana
    :expected: return a string with
    - full-width alphabet characters have been changed to half-width characters
    - kanji and katakana characters have bene changed to hiragana characters
    - hiragana characters have been kept as before
    """
    response = client.get("/common/get-pronunciation?text=Ｔシャツを着てみる")
    assert response.json() == "Tしゃつおきてみる"


def test_get_pronunciation_success_with_empty_string(client):
    """
    call API with an empty string
    :expected: return an empty string and status code is 200
    """
    response = client.get("/common/get-pronunciation?text=")
    assert response.status_code == 200
    assert response.json() == ""
