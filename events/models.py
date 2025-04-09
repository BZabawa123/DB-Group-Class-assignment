from django.db import models
from django.core.exceptions import ValidationError

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=80)
    category = models.CharField(
        max_length=20,
        choices=[
            ('Social', 'Social'),
            ('Fundraising', 'Fundraising'),
            ('Tech Talk', 'Tech Talk')
        ]
    )
    description = models.TextField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # Use string references for related apps
    lname = models.ForeignKey('locations.Locations', on_delete=models.DO_NOTHING, db_column='lname', null=True, blank=True)
    university = models.ForeignKey('universities.Universities', on_delete=models.DO_NOTHING, db_column='university_id')

    class Meta:
        db_table = 'Events'
        unique_together = (('lname', 'event_date', 'start_time'),)

    def clean(self):
        if self.lname is None:
            raise ValidationError("A location must be assigned for this event.")
        overlapping_events = Event.objects.filter(
            lname=self.lname,
            event_date=self.event_date,
        ).exclude(event_id=self.event_id)
        for event in overlapping_events:
            if (self.start_time < event.end_time) and (self.end_time > event.start_time):
                raise ValidationError(
                    f"Overlapping event: {event.event_name} from {event.start_time} to {event.end_time} at {self.lname}."
                )
        super().clean()

    def save(self, *args, **kwargs):
        if self.lname is None:
            from locations.models import Locations
            default_location = Locations.objects.first()
            if default_location is None:
                default_location = Locations.objects.create(
                    lname="DefaultLocation",
                    address="Default Address",
                    longitude=0.0,
                    latitude=0.0
                )
            self.lname = default_location
        self.full_clean()
        super().save(*args, **kwargs)

class EventCreation(models.Model):
    event = models.OneToOneField(Event, on_delete=models.DO_NOTHING, primary_key=True, db_column='event_id')
    admin = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING, related_name='admin_events', db_column='admin_id')
    superadmin = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING, related_name='superadmin_events', db_column='superadmin_id')
    privacy = models.CharField(max_length=10, choices=[('Public', 'Public'), ('Private', 'Private')])

    class Meta:
        db_table = 'Event_Creation'

class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING, db_column='uid')
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, db_column='event_id')
    rating = models.IntegerField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comments'
