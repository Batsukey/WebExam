from django import forms

from XroutS.activities.models import RunningActivity, GPSData, SwimmingActivity, CyclingActivity
from XroutS.core.models import UserProfile

class CyclingActivityForm(forms.ModelForm):
    class Meta:
        model = CyclingActivity
        fields = ['title','distance','duration','avg_speed','route','picture']
class RunningActivityForm(forms.ModelForm):
    class Meta:
        model = RunningActivity
        fields = ['title','distance','elevation','duration','pace','picture']


class SwimmingActivityForm(forms.ModelForm):
    class Meta:
        model = SwimmingActivity
        fields = ['title','distance','laps','duration','pool_length','picture']




class GPSDataUploadForm(forms.ModelForm):
    class Meta:
        model = GPSData
        fields = ['timestamp', 'latitude', 'longitude', 'elevation']

class GPXFileUploadForm(forms.Form):
    gpx_file = forms.FileField(label='Upload GPX File')