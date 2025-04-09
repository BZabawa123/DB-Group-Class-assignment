from django import forms
from .models import Users, Events, EventCreation, RSOs
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(forms.ModelForm):
    role = forms.ChoiceField(choices=Users.USER_ROLES)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['event_name', 'category', 'description', 'event_date', 'start_time', 'end_time', 'lname']

class EventPrivacyForm(forms.Form):
    privacy_choices = [
        ('Public', 'Public'),
        ('Private', 'Private'),
    ]
    privacy = forms.ChoiceField(choices=privacy_choices)
    rso = forms.ModelChoiceField(queryset=RSOs.objects.all(), required=False)  # Only for RSO even

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['event_name', 'category', 'description', 'event_date', 'start_time', 'end_time', 'lname']