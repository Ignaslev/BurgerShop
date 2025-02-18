from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .forms import UserUpdateForm, ProfileUpdateForm
from .models import User


def index(request):
    return render(request, 'index.html')


@csrf_protect
def register_user(request):
    if request.method == 'GET':
        return render(request, 'registration/registration.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_nr = request.POST.get('phone_nr')


        if password != password2:
            messages.error(request, "Passwords doesn't match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )

        customer_group = Group.objects.get(name='Customer')
        user.groups.add(customer_group)

        user.profile.phone = phone_nr
        user.profile.save()

        messages.info(request, f'Registration of {username} successful')
        return redirect('login')


@login_required
def get_user_profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.info(request, 'Profile updated')
        else:
            messages.error(request, 'Error')
        return redirect('user-profile')

    p_form = ProfileUpdateForm(instance=request.user.profile)
    u_form = UserUpdateForm(instance=request.user)

    context = {
        'p_form': p_form,
        'u_form': u_form
    }

    return render(request, 'profile.html', context=context)