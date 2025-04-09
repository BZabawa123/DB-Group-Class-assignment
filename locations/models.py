from django.db import models

class Locations(models.Model):
    lname = models.CharField(primary_key=True, max_length=80)
    address = models.CharField(max_length=80)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        db_table = 'Locations'
        managed = True

    def __str__(self):
        return self.lname
