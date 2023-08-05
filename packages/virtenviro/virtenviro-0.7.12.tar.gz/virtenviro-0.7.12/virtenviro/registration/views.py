#~*~ coding: utf-8 ~*~
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from virtenviro.registration.models import UserProfile
from virtenviro.registration.forms import UserForm, UserProfileForm


def signup(request):
    """Регистрация"""
    user = User()
    user_profile = UserProfile()
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_data = user_form.cleaned_data
            user.username = user_data['email']
            user.first_name = user_data['firstname']
            user.last_name = user_data['lastname']
            user.email = user_data['email']
            user.set_password(user_data['pass1'])
            user.save()

            user_profile = user.get_profile()
            user_profile_data = user_profile_form.cleaned_data
            user_profile.weight = user_profile_data['weight']
            user_profile.save()
            user = authenticate(username=user_data['username'], password=user_data['pass1'] )
            login(request, user)
            return redirect("/accounts/profile/")
    else:
        user_form = UserForm( instance = user )
        user_profile_form = UserProfileForm( instance = user_profile )
    return render(request,
                  "accounts/signup.html",
                  {
                      "user_": user,
                      "user_profile": user_profile,
                      "user_form": user_form,
                      "user_profile_form": user_profile_form})

@login_required
def profile(request):
    """Профиль текущего пользователя"""
    user = request.user
    return render(request,
                  "accounts/card.html",
                  {
                      "user": user})


@login_required
def user_card(request):
    """Профиль текущего пользователя"""
    user = request.user
    return render(request,
                  "accounts/card.html",
                  {"user": user})


@login_required
def logout(request):
    goto = request.GET.get("goto", "/")
    return redirect(goto)