from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def panel_main(request):
    return render(request, 'main/main_page.html')