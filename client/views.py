from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from payment.models import Order

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

@login_required
def u_profile(request):
    return render(request, 'main/profile.html')

@login_required
def payment_history(request):
    payments = Order.objects.order_by('-id').filter(user_id=request.user.id)
    return render(request, 'main/history.html', {'payments': payments})