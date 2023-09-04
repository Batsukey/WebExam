import datetime

from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models
from datetime import timedelta

from XroutS.core.models import AppUser
from XroutS.functionalities.models import Like



UserModel = get_user_model()

class DurationField(models.Field):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return timedelta(seconds=value)

    def to_python(self, value):
        if isinstance(value, timedelta):
            return value
        if value is None:
            return value
        return timedelta(seconds=value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        return int(value.total_seconds())

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_db_prep_value(value, None)
DISTANCE_CHOICES = [
    ('km', 'Kilometers'),
    ('m', 'meters'),
    ('mi', 'miles'),]
class BaseActivity(models.Model):
    picture = models.ImageField(
        blank=True,
        null=True
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    date_of_activity = models.DateField(blank=True, null=True)
    time = models.CharField(max_length=10, null=True, blank=True)  # Store time as "HH:MM AM/PM"
    distance = models.FloatField()
    duration = models.DurationField()
    title = models.CharField(max_length=30)
    likes = models.ManyToManyField(Like, blank=True)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.picture:
            print('Good')
            img = Image.open(self.picture.path)
            max_size = (800, 800)  # Define the maximum size for the image

            if img.width > max_size[0] or img.height > max_size[1]:
                img.thumbnail(max_size)
                img.save(self.picture.path)



class RunningActivity(BaseActivity):
    pace = models.DurationField()
    elevation = models.FloatField()
    def get_activity_type(self):
        return 'Running'



class CyclingActivity(BaseActivity):
    route = models.CharField(max_length=200)
    avg_speed = models.FloatField()
    def get_activity_type(self):
        return 'Cycling'

class SwimmingActivity(BaseActivity):
    pool_length = models.PositiveIntegerField()
    laps = models.PositiveIntegerField()

    def get_activity_type(self):
        return 'Swimming'
1
class ActivityData(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    type = models.CharField()
    name = models.CharField()
    distance = models.CharField()
    duration = models.CharField()
    pace = models.CharField()
    pace_chart_image = models.ImageField(upload_to='pace_charts/', blank=True, null=True)

class GPSData(models.Model):
    activity = models.ForeignKey(ActivityData, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.FloatField()
    hr = models.FloatField(null=True)
    distance = models.FloatField(null=True)
    cadance = models.FloatField(null=True)


    # def __str__(self):
    #     return f"{self.user.name} - {self.timestamp}"



