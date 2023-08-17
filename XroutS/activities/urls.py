from django.urls import path, include

from XroutS.activities.views import CreateActivity, ActivitiesFeedView, CreateRunningActivity, \
    CreateSwimmingActivity, CreateCyclingActivity, UploadGPXView, map_view, delete_activity, edit_activity

urlpatterns = [
    path('upload/',include([
        path('',CreateActivity.as_view(),name='create_activity'),
        path('running/',CreateRunningActivity.as_view(),name='running_activity'),
        path('swimming/',CreateSwimmingActivity.as_view(),name='swimming_activity'),
        path('cycling/',CreateCyclingActivity.as_view(),name='cycling_activity'),])),
    path('activityfeed/',ActivitiesFeedView.as_view(),name='activity_feed'),
    path('upload-activity/', UploadGPXView.as_view(), name='gps_upload'),
    path('activity/<str:activity_type>/<int:id>/delete/',delete_activity,name='delete_activity'),
    path('activity/<str:activity_type>/<int:id>/edit/',edit_activity,name='edit_activity'),
    # path('activityfeed/', running_map, name='running_map'),
    path('map/', map_view,name='map'),
    #
]