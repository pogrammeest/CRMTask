import json
import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class MyFirstsTestCase(APITestCase):
    custom_user_url = reverse('customs-users-list')

    def setUp(self):

        # создайте нового пользователя, отправив запрос к конечной точке djoser
        self.user = self.client.post('/auth/users/', data={'username': 'mario', 'password': 'i-keep-jumping', 'is_staff': 'true'})

        # получить веб-токен JSON для вновь созданного пользователя
        response = self.client.post('/auth/jwt/create/', data={'username': 'mario', 'password': 'i-keep-jumping'})

        self.user_id = self.user.data['id']
        self.token = response.data['access']

        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # получить список всех профилей пользователей во время аутентификации пользователя запроса
    def test_userprofile_list_authenticated(self):
        # print(reverse('user-list'))
        response = self.client.get(reverse('user-list'))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # получить список всех профилей пользователей, пока запрос пользователя не прошел проверку подлинности
    # def test_userprofile_list_unauthenticated(self):
    #     self.client.force_authenticate(user=None)
    #     response = self.client.get(self.custom_user_url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # проверьте, чтобы получить данные профиля аутентифицированного пользователя
    def test_userprofile_detail_retrieve(self):
        response = self.client.get(reverse('user-detail', kwargs={'id': self.user_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_custom_user_list_authenticated(self):
        # print(self.custom_user_url)
        response = self.client.get(self.custom_user_url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # заполнить профиль пользователя, который был автоматически создан с использованием сигналов
    def test_userprofile_profile(self):
        profile_data = {'date_of_birth': f'{datetime.date.today()}', 'user': self.user_id}
        response = self.client.put(reverse('customs-users-detail', kwargs={'pk': self.user_id}), data=profile_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_create(self):
        profile_data = {'title': 'Test'}
        response = self.client.post('/api/tasks/', data=profile_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



# class userProfileTestCase(APITestCase):
#     custom_user_url = reverse('all-profiles')
#
#     def setUp(self):
#         # создайте нового пользователя, отправив запрос к конечной точке djoser
#         self.user = self.client.post('/auth/users/', data={'username': 'mario', 'password': 'i-keep-jumping'})
#         # получить веб-токен JSON для вновь созданного пользователя
#         response = self.client.post('/auth/jwt/create/', data={'username': 'mario', 'password': 'i-keep-jumping'})
#         self.token = response.data['access']
#         self.api_authentication()
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     # получить список всех профилей пользователей во время аутентификации пользователя запроса
#     def test_userprofile_list_authenticated(self):
#         response = self.client.get(self.custom_user_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     # получить список всех профилей пользователей, пока запрос пользователя не прошел проверку подлинности
#     def test_userprofile_list_unauthenticated(self):
#         self.client.force_authenticate(user=None)
#         response = self.client.get(self.custom_user_url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     # проверьте, чтобы получить данные профиля аутентифицированного пользователя
#     def test_userprofile_detail_retrieve(self):
#         response = self.client.get(reverse('profile', kwargs={'pk': 1}))
#         # print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     # заполнить профиль пользователя, который был автоматически создан с использованием сигналов
#     def test_userprofile_profile(self):
#         profile_data = {'description': 'I am a very famous game character', 'location': 'nintendo world',
#                         'is_creator': 'true', }
#         response = self.client.put(reverse('profile', kwargs={'pk': 1}), data=profile_data)
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
