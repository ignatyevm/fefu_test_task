def test_create_profile_incorrect_full_name(client):
    body = {
        "guid": "00000000-0000-0000-0000-000000000001",
        "full_name": "absdbabsdabsdba",
        "scientometric_db": "scopus",
        "document_count": 0,
        "citation_count": 0,
        "h_index": 0,
        "url": "https://scopus.com"
    }
    response = client.post("/profiles", json=body)
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"] == "value_error"
    assert content["field"] == "full_name"
    assert content["loc"] == "body"


def test_create_profile_wrong_scientometric_db(client):
    body = {
        "guid": "00000000-0000-0000-0000-000000000001",
        "full_name": "Имя Фамилия Отчество",
        "scientometric_db": "WRONG_SCIENOMETRIC_DB",
        "document_count": 0,
        "citation_count": 0,
        "h_index": 0,
        "url": "https://scopus.com"
    }
    response = client.post("/profiles", json=body)
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"] == "value_error.const"
    assert content["field"] == "scientometric_db"
    assert content["loc"] == "body"


def test_create_profile_negative_document_count(client):
    body = {
        "guid": "00000000-0000-0000-0000-000000000001",
        "full_name": "Имя Фамилия Отчество",
        "scientometric_db": "scopus",
        "document_count": -10,
        "citation_count": 0,
        "h_index": 0,
        "url": "https://scopus.com"
    }
    response = client.post("/profiles", json=body)
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"] == "value_error.number.not_ge"
    assert content["field"] == "document_count"
    assert content["loc"] == "body"


def test_create_profile_negative_citation_count(client):
    body = {
        "guid": "00000000-0000-0000-0000-000000000001",
        "full_name": "Имя Фамилия Отчество",
        "scientometric_db": "scopus",
        "document_count": 0,
        "citation_count": -10,
        "h_index": 0,
        "url": "https://scopus.com"
    }
    response = client.post("/profiles", json=body)
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"] == "value_error.number.not_ge"
    assert content["field"] == "citation_count"
    assert content["loc"] == "body"


def test_create_profile_negative_h_index(client):
    body = {
        "guid": "00000000-0000-0000-0000-000000000001",
        "full_name": "Имя Фамилия Отчество",
        "scientometric_db": "scopus",
        "document_count": 0,
        "citation_count": 0,
        "h_index": -10,
        "url": "https://scopus.com"
    }
    response = client.post("/profiles", json=body)
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"] == "value_error.number.not_ge"
    assert content["field"] == "h_index"
    assert content["loc"] == "body"


def test_create_profile_incorrect_url(client):
    body = {
        "guid": "00000000-0000-0000-0000-000000000001",
        "full_name": "Имя Фамилия Отчество",
        "scientometric_db": "scopus",
        "document_count": 5,
        "citation_count": 10,
        "h_index": 15,
        "url": "https://incorrect_url"
    }
    response = client.post("/profiles", json=body)
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"].startswith("value_error.url")
    assert content["field"] == "url"
    assert content["loc"] == "body"


def test_create_profile_already_exists(client):
    body = {
        "guid": "00000000-0000-0000-0000-000000000001",
        "full_name": "Имя Фамилия Отчество",
        "scientometric_db": "scopus",
        "document_count": 5,
        "citation_count": 10,
        "h_index": 15,
        "url": "https://scopus.com"
    }
    response = client.post("/profiles", json=body)
    content = response.json()
    assert response.status_code == 409
    assert content["type"] == "profile.already_exists"


def test_create_profile_success(client):
    body = {
        "guid": "00000000-0000-0000-0000-00000000000150",
        "full_name": "Имя Фамилия Отчество",
        "scientometric_db": "scopus",
        "document_count": 5,
        "citation_count": 10,
        "h_index": 15,
        "url": "https://scopus.com"
    }
    response = client.post("/profiles", json=body)
    check_response = client.get(
        "/profiles/{}/?scientometric_database=scopus&fields=document_count&fields=citation_count".format(body["guid"]))
    check_content = check_response.json()
    assert response.status_code == 201
    assert check_response.status_code == 200
    assert check_content["full_name"] == body["full_name"]
    assert check_content["h_index"] == body["h_index"]
    assert check_content["document_count"] == body["document_count"]
    assert check_content["citation_count"] == body["citation_count"]
    assert check_content["url"] == body["url"]
