from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm, WeightSettingsForm,ProfileUpdateForm


def login(request):
    if request.user.is_authenticated:
        return redirect('fitplan:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('fitplan:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('fitplan:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('fitplan:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:weight_settings')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def account_delete(request):
    if request.method == "POST":
        request.user.delete()
        return redirect('fitplan:index')
    return redirect('accounts:delete_confirm')

@login_required
def delete_confirm(request):
    return render(request, 'accounts/account_delete.html')

@login_required
def profile_update(request):
    user = request.user

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'accounts/account_edit.html', context)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def weight_settings(request):
    user = request.user
    if request.method == 'POST':
        form = WeightSettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save() 
            return redirect('fitplan:index')
    else:
        form = WeightSettingsForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/weight_settings.html', context)

from django.contrib.auth.forms import PasswordChangeForm
from .forms import AccountUpdateForm

@login_required
def account_edit(request):
    user = request.user

    if request.method == "POST":
        form = AccountUpdateForm(request.POST, instance=user)
        pw_form = PasswordChangeForm(user, request.POST)

        # 아이디/이메일 정상 + 비밀번호 변경도 정상
        if form.is_valid() and pw_form.is_valid():
            form.save()
            pw_form.save()
            update_session_auth_hash(request, user)  # 비밀번호 바꿔도 로그인 유지

            return redirect('accounts:profile')

    else:
        form = AccountUpdateForm(instance=user)
        pw_form = PasswordChangeForm(user)

    context = {
        'form': form,
        'pw_form': pw_form,
    }
    return render(request, 'accounts/account_edit.html', context)