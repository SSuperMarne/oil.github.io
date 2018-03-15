from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from payment.models import Order
from .models import Statistic, Support
from .forms import SupportForm

@login_required
def panel_main(request):
    payments = Order.objects.filter(user_id=request.user.id).order_by('-id')[:5]
    return render(request, 'main/main_page.html', {"payments": payments})

@login_required
def panel_stats(request):
    stats = Statistic.objects.get(id=1)
    return render(request, 'main/statistic.html', {"stats": stats})

@login_required
def new_support(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            nickname = request.user.username
            email = request.user.email
            title = form.cleaned_data.get('title')
            text = form.cleaned_data.get('text')
            add = Support(nickname=nickname, email=email, title=title, text=text)
            add.save()
            messages.add_message(request, messages.INFO, "Запрос отправлен администрации! Вы получите ответ на e-mail, который указан в вашем профиле.")
    else:
        form = SupportForm()
    return render(request, 'main/support.html', {"form": form})