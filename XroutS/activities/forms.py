from django import forms

from XroutS.activities.models import RunningActivity, GPSData, SwimmingActivity, CyclingActivity, ActivityData
from XroutS.core.models import UserProfile
class CyclingActivityForm(forms.ModelForm):

    class Meta:
        model = CyclingActivity
        fields = ['title','distance','duration','avg_speed','route','picture','time']
class RunningActivityForm(forms.ModelForm):
    class Meta:
        model = RunningActivity
        fields = ['title','distance','elevation','duration','pace','picture','time']


class SwimmingActivityForm(forms.ModelForm):
    class Meta:
        model = SwimmingActivity
        fields = ['title','distance','laps','duration','pool_length','picture','time']




class GPSDataUploadForm(forms.ModelForm):
    class Meta:
        model = GPSData
        fields = ['timestamp', 'latitude', 'longitude', 'elevation', 'hr', 'distance', 'cadance','activity']

class GPXFileUploadForm(forms.Form):
    gpx_file = forms.FileField(label='Upload GPX File')

class ActivityDataForm(forms.ModelForm):
    class Meta:
        model=ActivityData
        fields=['duration','distance','pace']