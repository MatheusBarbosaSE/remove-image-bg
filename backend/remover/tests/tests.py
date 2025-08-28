from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class RemoveBackgroundStubTest(TestCase):
    def test_post_endpoint_exists(self):
        url = reverse("remove-background")
        resp = self.client.post(url, {})
        self.assertIn(resp.status_code, [200, 400])
