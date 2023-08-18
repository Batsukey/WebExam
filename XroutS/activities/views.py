import folium
from itertools import chain

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as gen_views
from django.contrib.auth.mixins import LoginRequiredMixin
from XroutS.activities.forms import GPXFileUploadForm, SwimmingActivityForm, CyclingActivityForm, \
    RunningActivityForm
from XroutS.activities.models import RunningActivity, GPSData, CyclingActivity, SwimmingActivity
from XroutS.core.models import UserProfile
import gpxpy
from django.shortcuts import render, redirect
from .forms import GPSDataUploadForm
from datetime import datetime, timedelta
from lxml import etree
from django.views.generic import View
from django.http import HttpResponse

# Create your views here.
UserModel = get_user_model()


class CreateActivity(LoginRequiredMixin,gen_views.TemplateView):
    template_name = 'activities/create_activity.html'


class CreateRunningActivity(LoginRequiredMixin,gen_views.CreateView):
    form_class = RunningActivityForm
    template_name = 'activities/running_form_fields.html'
    success_url = reverse_lazy('activity_feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CreateSwimmingActivity(LoginRequiredMixin,gen_views.CreateView):
    form_class = SwimmingActivityForm
    template_name = 'activities/swimming_form_fields.html'
    success_url = reverse_lazy('activity_feed')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)
class CreateCyclingActivity(LoginRequiredMixin,gen_views.CreateView):
    form_class = CyclingActivityForm
    template_name = 'activities/cycling_form_fields.html'
    success_url = reverse_lazy('activity_feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ActivitiesFeedView(LoginRequiredMixin, gen_views.ListView):
    template_name = 'activity_feed.html'  # Create this template
    context_object_name = 'all_activities'

    def get_queryset(self):
        user = self.request.user
        running_activities = RunningActivity.objects.filter(user=user)
        cycling_activities = CyclingActivity.objects.filter(user=user)
        swimming_activities = SwimmingActivity.objects.filter(user=user)
        all_activities = sorted(chain(running_activities, cycling_activities, swimming_activities),
                                key=lambda activity: activity.timestamp,
                                reverse=True)
        for activity in all_activities:
            activity.activity_type = activity.get_activity_type()

        return all_activities

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['user_full_name'] = f"{user_profile.first_name} {user_profile.last_name}"
        context['user_picture'] = user_profile.profile_picture
        return context

def delete_activity(request, activity_type, id):
    if activity_type == 'Running':
        model = RunningActivity
    elif activity_type == 'Cycling':
        model = CyclingActivity
    elif activity_type == 'Swimming':
        model = SwimmingActivity
    else:
        # Handle invalid activity_type here if needed
        pass

    activity = get_object_or_404(model, pk=id, user=request.user)
    activity.delete()

    return redirect('activity_feed')


def edit_activity(request, activity_type, id):
    if activity_type == 'Running':
        model = RunningActivity
        forms = RunningActivityForm
    elif activity_type == 'Cycling':
        model = CyclingActivity
        forms = CyclingActivityForm
    elif activity_type == 'Swimming':
        model = SwimmingActivity
        forms = SwimmingActivityForm
    else:
        # Handle invalid activity_type here if needed
        pass

    activity = get_object_or_404(model, pk=id, user=request.user)

    if request.method == 'POST':
        form = forms(request.POST,request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activity_feed')
    else:
        form = forms(instance=activity)

    context = {
        'form': form
    }

    return render(request, 'activities/activity_edit.html', context)

from datetime import datetime, timedelta
from lxml import etree
from django.shortcuts import render, redirect
from django.views import View
from .forms import GPXFileUploadForm
from .models import GPSData


class UploadGPXView(LoginRequiredMixin, View):
    template_name = 'upload_gps_data.html'

    def get(self, request, *args, **kwargs):
        gpx_form = GPXFileUploadForm()
        return render(request, self.template_name, {'gpx_form': gpx_form})

    def post(self, request, *args, **kwargs):
        gpx_form = GPXFileUploadForm(request.POST, request.FILES)
        if gpx_form.is_valid():
            gpx_file = gpx_form.cleaned_data['gpx_file']
            gpx_data = gpx_file.read()

            # Parse GPX data
            try:
                gpx = gpxpy.parse(gpx_data)
                filtered_data = []

                for track in gpx.tracks:
                    for segment in track.segments:
                        for point in segment.points:
                            # Filtering logic - adjust as needed
                            if point.time.second % 30 == 0:
                                filtered_data.append({
                                    'timestamp': point.time,
                                    'latitude': point.latitude,
                                    'longitude': point.longitude,
                                    'elevation': point.elevation,
                                })

                # Insert filtered data into the database
                try:
                    for data_point in filtered_data:
                        gps_data = GPSData.objects.create(
                            user=request.user,
                            timestamp=data_point['timestamp'],
                            latitude=data_point['latitude'],
                            longitude=data_point['longitude'],
                            elevation=data_point['elevation']
                        )
                    messages.success(request, 'GPX data uploaded successfully.')
                except Exception as e:
                    messages.error(request, f'Error uploading GPS data: {e}')
            except gpxpy.gpx.GPXXMLSyntaxException:
                messages.error(request, 'Invalid GPX file format.')

            return redirect('map')

        return render(request, self.template_name, {'gpx_form': gpx_form})


def map_view(request):
    # Retrieve GPS data from the database
    gps_data = GPSData.objects.filter(user=request.user)

    # Create a folium map centered at the first data point
    if gps_data:
        start_point = (gps_data.first().latitude, gps_data.first().longitude)
        my_map = folium.Map(location=start_point, zoom_start=15)

        # Create a polyline using all data points except the last one
        locations = [(point.latitude, point.longitude) for point in gps_data.exclude(id=gps_data.last().id)]
        folium.PolyLine(
            locations=locations,
            color='blue',
            weight=2,
            opacity=1
        ).add_to(my_map)

        # Add a flag icon for the finish marker
        finish_icon = folium.DivIcon(html='<div style="font-size: 13px;color: red;">🏁</div>')
        folium.Marker(
            location=(gps_data.last().latitude, gps_data.last().longitude),
            popup='Finish',
            icon=finish_icon
        ).add_to(my_map)

        # Create a green dot icon for the start point
        start_icon = folium.DivIcon(html='<div style="font-size: 25px;color: green;">●</div>')
        folium.Marker(
            location=(gps_data.first().latitude, gps_data.first().longitude),
            popup='Start',
            icon=start_icon
        ).add_to(my_map)

        map_html = my_map._repr_html_()

        return render(request, 'map.html', {'map_html': map_html})
    else:
        return render(request, 'map.html', {'map_html': ''})