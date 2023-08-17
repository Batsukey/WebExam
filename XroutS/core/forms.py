from django import forms

from XroutS.core.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name','age','city','profile_picture']

        labels = {
            'first_name': 'Name',
            'last_name': 'Surname',
            'age': 'Your age',
            'city': 'City',
            'profile_picture': 'Profile Picture',


        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First Name'
                }
            ),

        }