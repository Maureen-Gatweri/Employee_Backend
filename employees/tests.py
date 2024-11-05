from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from employees.models import Employee
from django.urls import reverse

class EmployeeAPITestCase(APITestCase):

    def setUp(self):
        # Create some initial data for testing
        self.employee = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            department="Engineering",
            position="Software Developer",
            hire_date="2022-01-01"
        )
        self.employee_url = reverse('employee_detail', kwargs={'pk': self.employee.id})
        self.list_url = reverse('employee_list')

    def test_get_all_employees(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)  # Check if at least one employee is returned

    def test_create_employee(self):
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "department": "Marketing",
            "position": "Marketing Specialist",
            "hire_date": "2023-05-01"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], "Jane")

    def test_get_employee_detail(self):
        response = self.client.get(self.employee_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "John")

    def test_update_employee(self):
        data = {
            "first_name": "Johnny",
            "last_name": "Doe",
            "department": "Engineering",
            "position": "Senior Developer",
            "hire_date": "2022-01-01"
        }
        response = self.client.put(self.employee_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Johnny")
        self.assertEqual(response.data['position'], "Senior Developer")

    def test_delete_employee(self):
        response = self.client.delete(self.employee_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure the employee no longer exists
        response = self.client.get(self.employee_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

