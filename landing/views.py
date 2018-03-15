from django.shortcuts import render, redirect

def landing_main(request):
    if request.user.is_authenticated:
        return redirect('panel_main')
    else:
        return render(request, 'landing/main.html')