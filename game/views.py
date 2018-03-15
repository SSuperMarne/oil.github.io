from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from payment.models import Order
from client.models import Profile
from .models import Statistic, Support
from .forms import SupportForm, ExchangeForm
import math

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

@login_required
def exchange(request):
    client = Profile.objects.get(user_id=request.user.id)
    client_rubs = lambda: math.floor(client.oil / 100)
    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        if form.is_valid():
            user_request = form.cleaned_data.get('rubs')
            server_check = client_rubs() - user_request
            if server_check < 0:
                messages.add_message(request, messages.ERROR, "У вас недостаточно нефти для получения указанного количества рублей.")
            else:
                convert = user_request * 100
                client.oil = client.oil - convert
                client.balance = client.balance + user_request
                client.save()
                messages.add_message(request, messages.INFO, "Операция успешно выполнена. Зачислено: " + str(user_request) + " руб.")
        else:
            messages.add_message(request, messages.ERROR, "Введено неверное значение. Действие отменено.")
    return render(request, 'main/exchanger.html', {'made': client_rubs()})