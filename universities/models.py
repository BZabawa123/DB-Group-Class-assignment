from django.db import models

class Universities(models.Model):
    university_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=80)
    description = models.TextField()
    number_of_students = models.IntegerField()

    class Meta:
        db_table = 'Universities'

    def __str__(self):
        return self.name
