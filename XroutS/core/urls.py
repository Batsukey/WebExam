from django.urls import path, include
from XroutS.core.views import RegisterUserView, HomePageView, LoginView, ProfileUpdateView, ProfileEditView, LogOutView, \
    AthleteDetailsPage, Custom404View, follow_user, unfollow_user

urlpatterns = [
    path('', HomePageView.as_view(),name='index'),
    path('register/', RegisterUserView.as_view(),name="register_user"),
    path('login/',LoginView.as_view(), name='login_user'),
    path('logout/',LogOutView.as_view(), name='logout_user'),
    path('404/', Custom404View.as_view(), name='custom_404'),
    path('athlete/<slug:athlete_slug>/',AthleteDetailsPage.as_view(),name='profile_details'),
    path('profile/update',ProfileUpdateView.as_view(),name='profile_update'),
    path('follow/<str:username>/', follow_user, name='follow_user'),
    path('unfollow/<str:username>/', unfollow_user, name='unfollow_user'),
]