import os

from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.contrib import messages

from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .forms import NewUserForm, UpdateProfileForm, UpdateUserForm
from .models import Profile

# Create your views here.


# newly added function
def update_user_data(user):
    Profile.objects.update_or_create(user=user, defaults={'phone': user.profile.phone})


def registerview(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            # newly added
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            dob = form.cleaned_data.get('dob')
            gender = form.cleaned_data.get('gender')
            # load the profile instance created by the signal
            user.save()

            profile = Profile(user=user, email=email, phone=phone, name=name, dob=dob, gender=gender)
            profile.save()
            raw_password = form.cleaned_data.get('password1')

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request,  user)

            # redirect user to home page
            return redirect('users-profile')
    else:
        form = NewUserForm()
    return render(request, 'account/register.html', {'form': form})


def loginview(request):
    if request.user.is_authenticated:
        return redirect('users-profile')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('users-profile')
            else:
                messages.info(request, "Username or Password is incorrect")


        context = {}
        return render(request, 'account/login.html', context)


def logoutview(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def homeview(request):
    context = {}
    return render(request, 'account/home.html', context)


@login_required
def userprofileview(request):

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'account/profile.html', {'user_form': user_form, 'profile_form': profile_form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'account/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')
