from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from payment.models import Order
from .models import Statistic

@login_required
def panel_main(request):
    payments = Order.objects.filter(user_id=request.user.id).order_by('-id')[:5]
    return render(request, 'main/main_page.html', {"payments": payments})

@login_required
def panel_stats(request):
    stats = Statistic.objects.get(id=1)
    return render(request, 'main/statistic.html', {"stats": stats})