from django.test import TestCase
from .models import Event

class EventsModelTest(TestCase):
    def test_event_creation(self):
        event = Event.objects.create(
            event_name="Sample Event",
            category="Social",
            description="This is a sample event.",
            event_date="2025-01-01",
            start_time="10:00:00",
            end_time="12:00:00",
            university_id=1  # You may need to create a Universities instance or adjust as appropriate
        )
        self.assertEqual(event.event_name, "Sample Event")
