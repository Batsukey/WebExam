from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import views as auth_views, get_user_model, login, authenticate
from django.contrib.auth import forms as auth_forms
from django.urls import reverse_lazy
from django.views import generic as views
from django import forms
from XroutS.core.forms import UserProfileForm

from XroutS.core.forms import UserProfileForm
from XroutS.core.models import UserProfile

UserModel = get_user_model()

# Create your views here.
class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-label', 'type': 'email'})
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = UserProfile(
            user=user,
        )
        if commit:
            profile.save()
        return user
class RegisterUserView(views.CreateView):
    template_name = 'auth/registration.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('profile_update')

    def form_valid(self, form):
        valid = super(RegisterUserView, self).form_valid(form)
        email, password = form.cleaned_data.get(
            'email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)

        return valid


class HomePageView(views.TemplateView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('activity_feed'))
        else:
            return super().get(request, *args, **kwargs)

    # Default template for logged-in users

    def get_template_names(self):
        # Check if the user is anonymous
        if self.request.user.is_anonymous:
            return ['index.html']
        return super().get_template_names()


class ActivityFeedView(views.CreateView):
    template_name = 'activity_feed.html'

class LoginView(auth_views.LoginView):
    template_name = 'auth/login.html'
    success_url = reverse_lazy('activity_feed')

class ProfileEditView(views.View):
    template_name = 'profile/profile_form.html'
    slug_field = 'athlete_slug'
    def get(self, request,athlete_slug):

        user = get_object_or_404(UserModel, slug=athlete_slug)

        try:
            user_profile = user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = None

        form = UserProfileForm(instance=user_profile)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, athlete_slug):
        user = get_object_or_404(UserModel, slug=athlete_slug)

        try:
            user_profile = user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = None

        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile')  # Redirect to the profile page or other URL

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)




class ProfileUpdateView(views.UpdateView):
    template_name = 'profile/profile_form.html'
    user = UserModel
    form_class = UserProfileForm
    @login_required
    def get(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(instance=user_profile)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    @login_required
    def post(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()




            return redirect('create_activity')  # Redirect to the profile page or other URL

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

class LogOutView(auth_views.LogoutView):
    template_name = 'auth/logout.html'
    success_url = reverse_lazy('activity_feed')

class AthleteDetailsPage(views.View):
    template_name = 'profile/details_user.html'
    def get(self, request, athlete_slug):
        user = get_object_or_404(UserModel,userprofile__slug=athlete_slug)

        try:
            user_profile = user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = None

        full_name = f"{user_profile.first_name} {user_profile.last_name}" if user_profile else ""

        context = {
            'picture': user_profile.profile_picture,
            'full_name': full_name,
        }

        return render(request, self.template_name, context)


class Custom404View(views.View):
    template_name = 'base/404.html'  # Path to your custom 404 template

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=404)