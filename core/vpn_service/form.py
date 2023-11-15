from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import UserProfile, UserSite


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class AddUserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['data_of_birth', 'phone_number']


class CreateSiteForm(ModelForm):
    class Meta:
        model = UserSite
        fields = ['user_site_name', 'original_site']