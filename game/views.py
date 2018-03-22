from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from payment.models import Order
from client.models import Profile, ReferralSys
from .models import Statistic, Support, Factory, Tower, ClientFactory, ClientTower, Advertisement
from .forms import SupportForm, ExchangeForm
import math
import time

@login_required
def panel_main(request):
    payments = Order.objects.filter(user_id=request.user.id).order_by('-id')[:5]
    ads = Advertisement.objects.order_by('id')
    refs = ReferralSys.objects.filter(id_referrer=request.user.id).order_by('-id')
    d = {'payments': payments, 'ads': ads, 'refs': refs}
    return render(request, 'main/main_page.html', {"d": d})

@login_required
def panel_stats(request):
    stats = Statistic.objects.get(id=1)
    users_count = Profile.objects.latest('id')
    return render(request, 'main/statistic.html', {"stats": stats, "user_c": users_count})

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

@login_required
def shop(request):
    factories = Factory.objects.order_by('id')[:5]
    towers = Tower.objects.order_by('id')[:5]
    return render(request, 'main/shop.html', {'factories': factories, 'towers': towers})

@login_required
def buy(request, category, goods):
    client = Profile.objects.get(user_id=request.user.id)
    timed = lambda: int(round(time.time() + 86400)) # 86400 sec. - 1 day
    if category == "0":
        # if category - Towers
        good = get_object_or_404(Tower, id=goods)
        if client.balance < good.price:
            messages.add_message(request, messages.ERROR, "У вас нет необходимой суммы для оплаты товара.")
        else:
            try:
                check = ClientFactory.objects.get(user_id=client.id, tower_id=good.id)
                data = ClientTower(tower_id_id=good.id, user_id=client.id, work=timed(), tower_name=good.name, tower_oil=good.oil)
                data.save()
                client.balance = client.balance - good.price
                client.stat_tower = client.stat_tower + 1 # user stat
                client.save()
                # Statistic global
                stat = Statistic.objects.get(id=1)
                stat.tower = stat.tower + 1
                stat.save()
                messages.add_message(request, messages.INFO, "Вы успешно приобрели товар.")
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, "Для покупки этой башни необходимо купить завод этого же типа.")
    elif category == "1":
        # if category - Factory
        good = get_object_or_404(Factory, id=goods)
        if client.balance < good.price:
            messages.add_message(request, messages.ERROR, "У вас нет необходимой суммы для оплаты товара.")
        else:
            try:
                check = ClientFactory.objects.get(user_id=client.id, factory_id=good.id)
                messages.add_message(request, messages.ERROR, "Этот завод у вас уже приобретен.")
            except ObjectDoesNotExist:
                data = ClientFactory(factory_id=good.id, name=good.name, user_id=client.id, tower_id=good.tower_id)
                data.save()
                client.balance = client.balance - good.price
                client.save()
                messages.add_message(request, messages.INFO, "Вы успешно приобрели товар.")
    return redirect('shop')

@login_required
def inventory(request):
    towers = ClientTower.objects.filter(user_id=request.user.id)
    return render(request, 'main/inventory.html', {'towers': towers})

@login_required
def get_oil(request, pk):
    timed = lambda: int(round(time.time()))
    try:
        a = ClientTower.objects.get(user_id=request.user.id, id=pk)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Запрос выполнен неверно. Свяжитесь с администрацией магазина.")
        return redirect('inventory')
    client = Profile.objects.get(user_id=request.user.id)
    if timed() - a.work >= 0:
        client.oil = client.oil + a.tower_oil
        client.stat_produced = client.stat_produced + a.tower_oil # stats
        client.save()
        a.work = timed() + 86400
        a.save()
        # Statistic global
        stat = Statistic.objects.get(id=1)
        stat.oil = stat.oil + a.tower_oil
        stat.save()
        messages.add_message(request, messages.INFO, "Нефть успешно собрана.")
    else:
        messages.add_message(request, messages.ERROR, "Прошло недостаточно времени для выдачи нефти.")
    return redirect('inventory')