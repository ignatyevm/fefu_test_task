def test_get_statistics(client):
    response = client.get("/publication_activity_statistics")
    content = response.json()
    assert response.status_code == 200
    expected = {
        "risc": {
            "total_document_count": 10225,
            "total_citation_count": 66691,
            "average_h_index": 54.2
        },
        "wos": {
            "total_document_count": 1854,
            "total_citation_count": 61315,
            "average_h_index": 34.4
        },
        "scopus": {
            "total_document_count": 3368,
            "total_citation_count": 177083,
            "average_h_index": 62.6
        },
    }
    for statistics in content:
        expected_statistics = expected[statistics["scientometric_db"]]
        assert statistics["total_document_count"] == expected_statistics["total_document_count"]
        assert statistics["total_citation_count"] == expected_statistics["total_citation_count"]
        assert statistics["average_h_index"] == expected_statistics["average_h_index"]
