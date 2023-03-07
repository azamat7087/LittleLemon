from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.restaurant1 = Restaurant.objects.create(
            name='Restaurant 1',
            address='123 Main St',
            phone_number='555-1234',
            description='A nice place to eat.'
        )
        self.restaurant2 = Restaurant.objects.create(
            name='Restaurant 2',
            address='456 Oak Ave',
            phone_number='555-5678',
            description='Another nice place to eat.'
        )

    def test_get_all_restaurants(self):
        response = self.client.get(reverse('restaurant-list'))
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_restaurant(self):
        response = self.client.get(reverse('restaurant-detail', kwargs={'pk': self.restaurant1.pk}))
        restaurant = Restaurant.objects.get(pk=self.restaurant1.pk)
        serializer = RestaurantSerializer(restaurant)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_restaurant(self):
        data = {
            'name': 'Restaurant 3',
            'address': '789 Elm St',
            'phone_number': '555-9012',
            'description': 'A new place to eat.'
        }
        response = self.client.post(reverse('restaurant-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 3)
        restaurant = Restaurant.objects.get(name=data['name'])
        serializer = RestaurantSerializer(restaurant)
        self.assertEqual(response.data, serializer.data)

    def test_update_existing_restaurant(self):
        data = {
            'name': 'Updated Restaurant 1',
            'address': '123 Main St',
            'phone_number': '555-1234',
            'description': 'An updated description.'
        }
        response = self.client.put(reverse('restaurant-detail', kwargs={'pk': self.restaurant1.pk}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), 2)
        restaurant = Restaurant.objects.get(pk=self.restaurant1.pk)
        self.assertEqual(restaurant.name, data['name'])
        self.assertEqual(restaurant.description, data['description'])

    def test_delete_existing_restaurant(self):
        response = self.client.delete(reverse('restaurant-detail', kwargs={'pk': self.restaurant1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Restaurant.objects.count(), 1)
