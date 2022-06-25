
from django import forms
from django.db import models
from django.contrib.auth.models import User

from account.models import Profile

from django.contrib.auth.forms import UserCreationForm

from datetime import date


class NewUserForm(UserCreationForm):
   # email = forms.EmailField()
    # newly added
    name = forms.CharField()
    phone = forms.RegexField(regex=r'^[6-9]\d{9}$')
    dob = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), )

    CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    # gender = forms.CharField(label='Gender', widget=forms.RadioSelect(choices=CHOICES))
    gender = forms.CharField(widget=forms.widgets.Select(choices=CHOICES))

    def clean_dob(self):
        birth_date = self.cleaned_data['dob']
        age = (date.today() - birth_date).days/365
        if age < 18:
            raise forms.ValidationError('Must be atleast 18 years old to register')
        return birth_date

    class Meta:
        model = User
        fields = ['username', 'name', 'gender', 'email',  'phone', 'dob', 'password1', 'password2',]
        labels = {'phone': 'Mobile Number', 'name': 'Name', 'dob': 'DOB', 'gender': 'gender'}


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    dob = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), )
    # email = forms.EmailField(required=True,
    #                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_dob(self):
        birth_date = self.cleaned_data['dob']
        age = (date.today() - birth_date).days/365
        if age < 18:
            raise forms.ValidationError('Must be atleast 18 years old to register')
        return birth_date

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'dob', 'phone', 'gender', 'email']