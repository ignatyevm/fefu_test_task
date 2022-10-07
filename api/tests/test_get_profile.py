def test_get_profile_profile_not_found(client):
    guid = "00000000-0000-0000-0000-00000000000150"
    response = client.get(
        "/profiles/{}/?scientometric_database=scopus".format(guid))
    content = response.json()
    assert response.status_code == 404
    assert content["type"] == "profile.not_found"


def test_get_profile_profile_wrong_scientometric_db(client):
    guid = "00000000-0000-0000-0000-00000000000150"
    response = client.get(
        "/profiles/{}/?scientometric_database=WRONG_SCIENOMETRIC_DB".format(guid))
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"] == "value_error.const"
    assert content["field"] == "scientometric_database"
    assert content["loc"] == "query"


def test_get_profile_success_scopus(client):
    guid = "00000000-0000-0000-0000-000000000001"
    response = client.get(
        "/profiles/{}/?scientometric_database=scopus".format(guid))
    content = response.json()
    assert response.status_code == 200
    assert content["full_name"] == "Иванов Юрий Борисович"
    assert content["h_index"] == 115
    assert content["url"] == "https://www.scopus.com/authid/detail.uri?authorId=35221660700"


def test_get_profile_success_wos(client):
    guid = "00000000-0000-0000-0000-000000000006"
    response = client.get(
        "/profiles/{}/?scientometric_database=wos".format(guid))
    content = response.json()
    assert response.status_code == 200
    assert content["full_name"] == "Михайлов Сергей Иванович"
    assert content["h_index"] == 15
    assert content["url"] == "https://www.webofscience.com/wos/woscc/basic-search"


def test_get_profile_success_risc(client):
    guid = "00000000-0000-0000-0000-000000000009"
    response = client.get(
        "/profiles/{}/?scientometric_database=risc".format(guid))
    content = response.json()
    assert response.status_code == 200
    assert content["full_name"] == "Ильин Николай Александрович"
    assert content["h_index"] == 17
    assert content["url"] == "https://elibrary.ru/project_author_tools.asp?"


def test_get_profile_success_scopus_document_count(client):
    guid = "00000000-0000-0000-0000-000000000001"
    response = client.get(
        "/profiles/{}/?scientometric_database=scopus&fields=document_count".format(guid))
    content = response.json()
    assert response.status_code == 200
    assert content["full_name"] == "Иванов Юрий Борисович"
    assert content["h_index"] == 115
    assert content["url"] == "https://www.scopus.com/authid/detail.uri?authorId=35221660700"
    assert content["document_count"] == 1143


def test_get_profile_success_scopus_citation_count(client):
    guid = "00000000-0000-0000-0000-000000000001"
    response = client.get(
        "/profiles/{}/?scientometric_database=scopus&fields=citation_count".format(guid))
    content = response.json()
    assert response.status_code == 200
    assert content["full_name"] == "Иванов Юрий Борисович"
    assert content["h_index"] == 115
    assert content["url"] == "https://www.scopus.com/authid/detail.uri?authorId=35221660700"
    assert content["citation_count"] == 75891


def test_get_profile_success_scopus_document_count_and_citation_count(client):
    guid = "00000000-0000-0000-0000-000000000001"
    response = client.get(
        "/profiles/{}/?scientometric_database=scopus&fields=document_count&fields=citation_count".format(guid))
    content = response.json()
    assert response.status_code == 200
    assert content["full_name"] == "Иванов Юрий Борисович"
    assert content["h_index"] == 115
    assert content["url"] == "https://www.scopus.com/authid/detail.uri?authorId=35221660700"
    assert content["document_count"] == 1143
    assert content["citation_count"] == 75891
