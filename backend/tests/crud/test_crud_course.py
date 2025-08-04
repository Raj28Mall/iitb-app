def test_get_departments_endpoint(client):
    response = client.get("/api/v1/get_documents/test")
    assert response.status_code == 200