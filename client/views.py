from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # need change it to main (after auth)
            return redirect('landing_main')
        else:
            return render(request, 'registration/registration.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'registration/registration.html', {'form': form})

def u_profile(request):
    return render(request, 'main/profile.html')