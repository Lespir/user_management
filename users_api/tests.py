from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users_api.models import User as UserAPI
from users_api.serializers import UserSerializer


class UserTests(APITestCase):

    def setUp(self):

        user_test = User.objects.create_user(username='Tester', password='123')
        user_test.save()

        self.user_test_token = Token.objects.create(user=user_test)

        self.first_user = UserAPI.objects.create(
            uuid_ref='5a1b835c-515a-43fb-8ae2-b2b3435b451c',
            username='TestUser',
            email='test@user.email',
            age=23,
            nationality='Russian'
        )
        self.url_update = f'/api/v1/users_update/{self.first_user.uuid_ref}/'
        self.url_delete = f'/api/v1/users_delete/{self.first_user.uuid_ref}/'

        self.second_user = UserAPI.objects.create(
            uuid_ref='4eab40a4-dd87-483d-b25e-f4219bea8621',
            username='TestUser2',
            email='test2@user.email',
            age=35,
            nationality='China'
        )

        self.data = {
            "uuid_ref": "",
            "username": "TestUser3",
            "email": "test3@user.email",
            "age": 18,
            "nationality": "India"
        }

    def test_user_list(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_fail_user_detail(self):
        response = self.client.get(reverse('user_detail', kwargs={'pk': 'non-existent key'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_detail(self):
        response = self.client.get(reverse('user_detail', kwargs={'pk': self.first_user.uuid_ref}))
        serializer_data = UserSerializer(self.first_user).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_unauthorized_create_user(self):
        response = self.client.post(reverse('user_create'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test_token.key)
        response = self.client.post(reverse('user_create'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_update_user_put(self):
        response = self.client.put(
            self.url_update,
            data={
                "username": "new_name",
                "email": "new@email.test",
                "age": 24
            }, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_update_user_put(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test_token.key)
        response = self.client.put(
            self.url_update,
            data={
                "username": "new_name",
                "email": "new@email.test",
                "age": 24
            }, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.first_user.refresh_from_db()
        serializer_data = UserSerializer(self.first_user).data
        self.assertEqual(serializer_data, response.data)

    def test_unauthorized_update_user_patch(self):
        response = self.client.patch(self.url_update, data={"age": 25}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_update_user_patch(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test_token.key)
        response = self.client.patch(self.url_update, data={"age": 25}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['age'], 25)
        self.first_user.refresh_from_db()
        self.assertEqual(self.first_user.age, 25)

    def test_unauthorized_delete_user(self):
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test_token.key)
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
