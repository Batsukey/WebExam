from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect

from XroutS.activities.models import RunningActivity, CyclingActivity, SwimmingActivity
from XroutS.functionalities.models import Like

@login_required
def like_activity(request, activity_type, id):
    if activity_type == 'running':
        model = RunningActivity
    elif activity_type == 'cycling':
        model = CyclingActivity
    elif activity_type == 'swimming':
        model = SwimmingActivity

    activity = get_object_or_404(model, pk=id)

    user = request.user
    like, created = Like.objects.get_or_create(user=user)

    if like in activity.likes.all():
        activity.likes.remove(like)
    else:
        activity.likes.add(like)

    return redirect('activity_feed')