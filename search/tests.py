from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import json

class SearchAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_search_success(self):
        response = self.client.post('/api/search/', {'search_type': 'repositories', 'search_text': 'Django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_invalid_type(self):
        response = self.client.post('/api/search/', {'search_type': 'invalid', 'search_text': 'Django'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_missing_text(self):
        response = self.client.post('/api/search/', {'search_type': 'repositories'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clear_cache(self):
        self.client.post('/api/search/', {'search_type': 'repositories', 'search_text': 'Django'})
        response = self.client.post('/api/clear-cache/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
