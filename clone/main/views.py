from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile
from .models import Smeep
from .forms import SmeepForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        form = SmeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                smeep = form.save(commit=False)
                smeep.user = request.user
                smeep.save()
                messages.success(request, 'Your smeep has been submitted')
                return redirect('home')
        smeeps = Smeep.objects.all().order_by('-created_at')
        return render(request, 'main/home.html', {'smeeps': smeeps, "form": form})
    else:
        smeeps = Smeep.objects.all().order_by('-created_at')
        return render(request, 'main/home.html', {'smeep': smeeps})


def profile_list(request):
    if request.user.is_authenticated:

        # Exclude user from seeing himself
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'main/home.html', {"profiles": profiles})

    else:
        messages.success(request, ('You must be loggged in to see messages'))
        return render(request,'main/home.html')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        smeeps = Smeep.objects.filter(user_id=pk)

        # Post for logic
        if request.method == "POST":
            # Get current user
            current_user_profile = request.user.profile
            # Get from data
            action = request.POST['follow']
            # Decide to follow or unfollow

            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
                # Save the profile
                current_user_profile.save()

        return render(request, 'main/profile.html', {'profile': profile, 'smeeps': smeeps})
    else:
        messages.success(request, ('You must be logged in to see messages'))
        return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in.'))
            return redirect('home')
        else:
            messages.success(request, ('There was an error, please try again'))
            return redirect('login')
    else:
        return render(request, 'main/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out.'))
    return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = SignUpForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request,'Your profle changes has been saved')
            return redirect('home')

        return render(request, 'main/update_user.html',{'form':form})
    else:
        messages.success(request, ('You must be logged in to see this'))
        return redirect('home')





def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # first_name = form.cleaned_data['last_name']
            # first_name = form.cleaned_data['email']
            # Log in user
            user = authenticate(username = username, password=password)
            messages.success(request,('You have been successfully registered.'))
            login(request,user)
            return redirect('home')
    return render(request, "main/register.html", {'form':form})
