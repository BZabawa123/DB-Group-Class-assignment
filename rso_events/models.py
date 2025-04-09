from django.db import models

class RSOs(models.Model):
    rso_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    university = models.ForeignKey('universities.Universities', on_delete=models.CASCADE, db_column='university_id')
    admin = models.ForeignKey('accounts.Users', on_delete=models.CASCADE, related_name='admin_of_rsos', db_column='admin_id')
    members = models.ManyToManyField('accounts.Users', through='StudentsRSOs', related_name='member_of_rsos')
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive')

    class Meta:
        db_table = 'RSOs'

    def update_status(self):
        if self.members.count() >= 5:
            self.status = 'active'
        else:
            self.status = 'inactive'
        self.save()

    def __str__(self):
        return self.name

class StudentsRSOs(models.Model):
    uid = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    rso = models.ForeignKey(RSOs, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Students_RSOs'
        unique_together = ('uid', 'rso')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.rso.update_status()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.rso.update_status()

class RSOEvents(models.Model):
    event = models.OneToOneField('events.Event', on_delete=models.DO_NOTHING, primary_key=True, db_column='event_id')
    rso = models.ForeignKey(RSOs, on_delete=models.DO_NOTHING, db_column='rso_id')

    class Meta:
        db_table = 'RSO_Events'
