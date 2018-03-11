from django.shortcuts import render

def landing_main(request):
    return render(request, 'landing/main.html')