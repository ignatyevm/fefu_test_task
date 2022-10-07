def test_get_profiles_negative_limit(client):
    response = client.get("/profiles/?scientometric_database=scopus&limit=-10")
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"] == "value_error.number.not_ge"
    assert content["field"] == "limit"
    assert content["loc"] == "query"


def test_get_profiles_negative_offset(client):
    response = client.get("/profiles/?scientometric_database=scopus&offset=-10")
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"] == "value_error.number.not_ge"
    assert content["field"] == "offset"
    assert content["loc"] == "query"


def test_get_profiles_wrong_scientometric_database(client):
    response = client.get("/profiles/?scientometric_database=WRONG_SCIENOMETRIC_DB")
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"] == "value_error.const"
    assert content["field"] == "scientometric_database"
    assert content["loc"] == "query"


def test_get_profiles_wrong_order_by(client):
    response = client.get("/profiles/?scientometric_database=scopus&order_by=WRONG_FIELD")
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"] == "value_error.const"
    assert content["field"] == "order_by"
    assert content["loc"] == "query"


def test_get_profiles_wrong_order_dir(client):
    response = client.get("/profiles/?scientometric_database=scopus&order_by=date&order_dir=WRONG_DIR")
    content = response.json()[0]
    assert response.status_code == 400
    assert content["type"] == "value_error.const"
    assert content["field"] == "order_dir"
    assert content["loc"] == "query"


def test_get_profiles_default_wos(client):
    expected = {"profiles": [{"full_name": "Михайлов Сергей Иванович", "h_index": 15,
                              "url": "https://www.webofscience.com/wos/woscc/basic-search"},
                             {"full_name": "Иванов Юрий Борисович", "h_index": 92,
                              "url": "https://www.webofscience.com/wos/woscc/basic-search"},
                             {"full_name": "Смирнова Полина Викторовна", "h_index": 19,
                              "url": "https://www.webofscience.com/wos/woscc/basic-search"},
                             {"full_name": "Петров Олег Федорович", "h_index": 37,
                              "url": "https://www.webofscience.com/wos/woscc/basic-search"},
                             {"full_name": "Огнева Валентина Андреевна", "h_index": 9,
                              "url": "https://www.webofscience.com/wos/woscc/basic-search"}]}
    response = client.get("/profiles/?scientometric_database=wos")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_profiles_default_risc(client):
    expected = {"profiles": [{"full_name": "Огнева Валентина Андреевна", "h_index": 19,
                              "url": "https://elibrary.ru/project_author_tools.asp?"},
                             {"full_name": "Петров Олег Федорович", "h_index": 123,
                              "url": "https://elibrary.ru/project_author_tools.asp?"},
                             {"full_name": "Ильин Николай Александрович", "h_index": 17,
                              "url": "https://elibrary.ru/project_author_tools.asp?"},
                             {"full_name": "Иванов Юрий Борисович", "h_index": 67,
                              "url": "https://elibrary.ru/project_author_tools.asp?"},
                             {"full_name": "Иванов Василий Андреевич", "h_index": 45,
                              "url": "https://elibrary.ru/project_author_tools.asp?"}]}
    response = client.get("/profiles/?scientometric_database=risc")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_profiles_default_scopus(client):
    expected = {
        "profiles": [
            {"full_name": "Иванов Юрий Борисович", "h_index": 115,
             "url": "https://www.scopus.com/authid/detail.uri?authorId=35221660700"},
            {"full_name": "Иванов Василий Андреевич", "h_index": 14,
             "url": "https://www.scopus.com/authid/detail.uri?authorId=7404809618"},
            {"full_name": "Иванов Михаил Владимирович", "h_index": 24,
             "url": "https://www.scopus.com/authid/detail.uri?authorId=7201382133"},
            {"full_name": "Петров Владимир Алексеевич", "h_index": 117,
             "url": "https://www.scopus.com/authid/detail.uri?authorId=8049867900"},
            {"full_name": "Петров Олег Федорович", "h_index": 43,
             "url": "https://www.scopus.com/authid/detail.uri?authorId=7102305944"}
        ]
    }
    response = client.get("/profiles/?scientometric_database=scopus")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_profiles_limit2(client):
    expected = {
        "profiles": [
            {"full_name": "Иванов Юрий Борисович", "h_index": 115,
             "url": "https://www.scopus.com/authid/detail.uri?authorId=35221660700"},
            {"full_name": "Иванов Василий Андреевич", "h_index": 14,
             "url": "https://www.scopus.com/authid/detail.uri?authorId=7404809618"},
        ]
    }
    response = client.get("/profiles/?scientometric_database=scopus&limit=2")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_profiles_limit2_and_offset2(client):
    expected = {
        "profiles": [
            {"full_name": "Иванов Михаил Владимирович", "h_index": 24,
             "url": "https://www.scopus.com/authid/detail.uri?authorId=7201382133"},
            {"full_name": "Петров Владимир Алексеевич", "h_index": 117,
             "url": "https://www.scopus.com/authid/detail.uri?authorId=8049867900"},
        ]
    }
    response = client.get("/profiles/?scientometric_database=scopus&limit=2&offset=2")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_profiles_max_offset(client):
    expected = {
        "profiles": []
    }
    response = client.get("/profiles/?scientometric_database=scopus&offset=10")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_profiles_order_by_date_asc(client):
    expected = {"profiles": [{"full_name": "Иванов Юрий Борисович", "h_index": 115,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=35221660700"},
                             {"full_name": "Иванов Василий Андреевич", "h_index": 14,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7404809618"},
                             {"full_name": "Иванов Михаил Владимирович", "h_index": 24,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7201382133"},
                             {"full_name": "Петров Владимир Алексеевич", "h_index": 117,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=8049867900"},
                             {"full_name": "Петров Олег Федорович", "h_index": 43,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7102305944"}]}
    response = client.get("/profiles/?scientometric_database=scopus&order_by=date&order_dir=asc")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_profiles_order_by_date_desc(client):
    expected = {"profiles": [{"full_name": "Петров Олег Федорович", "h_index": 43,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7102305944"},
                             {"full_name": "Петров Владимир Алексеевич", "h_index": 117,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=8049867900"},
                             {"full_name": "Иванов Михаил Владимирович", "h_index": 24,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7201382133"},
                             {"full_name": "Иванов Василий Андреевич", "h_index": 14,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7404809618"},
                             {"full_name": "Иванов Юрий Борисович", "h_index": 115,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=35221660700"}]}
    response = client.get("/profiles/?scientometric_database=scopus&order_by=date&order_dir=desc")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_profiles_order_by_h_index_asc(client):
    expected = {"profiles": [{"full_name": "Иванов Василий Андреевич", "h_index": 14,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7404809618"},
                             {"full_name": "Иванов Михаил Владимирович", "h_index": 24,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7201382133"},
                             {"full_name": "Петров Олег Федорович", "h_index": 43,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7102305944"},
                             {"full_name": "Иванов Юрий Борисович", "h_index": 115,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=35221660700"},
                             {"full_name": "Петров Владимир Алексеевич", "h_index": 117,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=8049867900"}]}
    response = client.get("/profiles/?scientometric_database=scopus&order_by=h_index&order_dir=asc")
    assert response.status_code == 200
    assert response.json() == expected


def test_get_profiles_order_by_h_index_desc(client):
    expected = {"profiles": [{"full_name": "Петров Владимир Алексеевич", "h_index": 117,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=8049867900"},
                             {"full_name": "Иванов Юрий Борисович", "h_index": 115,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=35221660700"},
                             {"full_name": "Петров Олег Федорович", "h_index": 43,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7102305944"},
                             {"full_name": "Иванов Михаил Владимирович", "h_index": 24,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7201382133"},
                             {"full_name": "Иванов Василий Андреевич", "h_index": 14,
                              "url": "https://www.scopus.com/authid/detail.uri?authorId=7404809618"}]}
    response = client.get("/profiles/?scientometric_database=scopus&order_by=h_index&order_dir=desc")
    assert response.status_code == 200
    assert response.json() == expected
