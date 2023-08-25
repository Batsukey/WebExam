from django.urls import path

from XroutS.functionalities.views import like_activity

urlpatterns = [
    path('activity/<str:activity_type>/<int:id>/like/', like_activity, name='like_activity'),
    # path('',comment,name='comment_activity'),
]