from django.test import TestCase
from .models import RSOs

class RSOsModelTest(TestCase):
    def test_rso_str(self):
        rso = RSOs.objects.create(name="TestRSO", university_id=1, admin_id=1)
        self.assertEqual(str(rso), "TestRSO")
