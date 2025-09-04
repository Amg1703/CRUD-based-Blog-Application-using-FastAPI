from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_create_blog():
    response = client.post("/blog/", json={"blog_title": "Test Blog", "blog_body": "Test Content"})
    assert response.status_code == 200
    data = response.json()
    assert data["blog_title"] == "Test Blog"
    assert data["blog_body"] == "Test Content"

def test_get_all_blogs():
    response = client.get("/getallblogs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_blogs_by_wrong_id():
    response = client.get("/getblogsbyid/99999")
    assert response.status_code == 404

