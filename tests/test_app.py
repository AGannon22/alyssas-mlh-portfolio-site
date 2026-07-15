# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app, mydb, TimelinePost

class AppTestCase(unittest.TestCase):
    def setUp(self):
        mydb.connect(reuse_if_open=True)
        mydb.create_tables([TimelinePost])
        self.client = app.test_client()

    def tearDown(self):
        mydb.drop_tables([TimelinePost])
        if not mydb.is_closed():
            mydb.close()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Alyssa Gannon</title>" in html
        assert "About Me" in html
        assert "Alyssa" in html
        assert 'href="/timeline"' in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        post_response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": "Hello world, I'm John!"
        })
        assert post_response.status_code == 200
        assert post_response.is_json
        created_post = post_response.get_json()
        assert created_post["name"] == "John Doe"
        assert created_post["email"] == "john@example.com"
        assert created_post["content"] == "Hello world, I'm John!"
        assert "id" in created_post
        assert "created_at" in created_post

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "John Doe"
        assert json["timeline_posts"][0]["email"] == "john@example.com"
        assert json["timeline_posts"][0]["content"] == "Hello world, I'm John!"

        timeline_response = self.client.get("/timeline")
        assert timeline_response.status_code == 200
        timeline_html = timeline_response.get_data(as_text=True)
        assert "Timeline Posts" in timeline_html
        assert "John Doe" in timeline_html
        assert "Hello world, I&#39;m John!" in timeline_html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data=
    {"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data=
    {"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data=
    {"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html