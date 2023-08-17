from django.contrib.auth import get_user_model
from django.db import models

from XroutS.activities.models import AllActivities

UserModel = get_user_model()
# Create your models here.
class CommentActivity(models.Model):
    text = models.TextField(
        max_length=250,
        null=False,
        blank=False
    )
    date_of_publication = models.DateTimeField(
        auto_created=True,
        editable=False
    )
    date_of_edit = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        editable=False

    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )
    activity = models.ForeignKey(
        AllActivities,
        on_delete=models.CASCADE
    )

class Like(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    activity = models.ForeignKey(AllActivities, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)