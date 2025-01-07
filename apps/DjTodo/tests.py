from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import DjTodo
from django.contrib.auth.models import User

class DjTodoAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_todo(self):
        response = self.client.post('/api/create/', {'title': 'Test Todo', 'user':self.user.id, 'description': 'Test Description', 'is_completed': False})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DjTodo.objects.count(), 1)
        self.assertEqual(DjTodo.objects.get().title, 'Test Todo')

    def test_get_todos(self):
        DjTodo.objects.create(title='Test Todo 1', description='Test Description 1', user=self.user)
        DjTodo.objects.create(title='Test Todo 2', description='Test Description 2', user=self.user)
        response = self.client.get('/api/all-todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_todo(self):
        todo = DjTodo.objects.create(title='Test Todo', description='Test Description', user=self.user)
        response = self.client.delete(f'/api/delete/{todo.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DjTodo.objects.count(), 0)

    def test_get_specific_todo(self):
        todo = DjTodo.objects.create(title='Test Todo', description='Test Description', user=self.user, is_completed=True)
        response = self.client.get(f'/api/get-todo/{todo.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Todo')
