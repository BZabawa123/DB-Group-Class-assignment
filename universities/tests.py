from django.test import TestCase
from .models import Universities

class UniversitiesModelTest(TestCase):
    def test_university_str(self):
        uni = Universities.objects.create(name="Test University", location="Test City", description="A test institution", number_of_students=1000)
        self.assertEqual(str(uni), "Test University")
