from django.test import SimpleTestCase, override_settings


@override_settings(ALLOWED_HOSTS=["testserver"])
class ViewTests(SimpleTestCase):
    def test_index(self):
        response = self.client.get("/", secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_health_works_over_plain_http(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})

    def test_http_is_redirected_to_https(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 301)
        self.assertTrue(response["Location"].startswith("https://"))

    def test_unknown_host_is_rejected(self):
        response = self.client.get("/", secure=True, HTTP_HOST="evil.example")
        self.assertEqual(response.status_code, 400)

    def test_debug_is_off(self):
        from django.conf import settings

        self.assertFalse(settings.DEBUG)
