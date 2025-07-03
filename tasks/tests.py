from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken  # ✅ Needed for token creation

class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # ✅ Generate access token
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # ✅ Set the Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_create_task(self):
        data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "completed": False
        }
        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_task(self):
        task = Task.objects.create(
            title="Old Task", description="Old", completed=False, user=self.user
        )
        data = {
            "title": "Updated Task",
            "description": "Updated",
            "completed": True
        }
        url = f'/api/tasks/{task.id}/'
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
