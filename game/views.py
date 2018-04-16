from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from payment.models import Order
from client.models import Profile, ReferralSys, Transfer
from .models import Statistic, Factory, Tower, ClientFactory, ClientTower, Advertisement, TowerLevel
from .forms import ExchangeForm
import math
import time

@login_required
def panel_main(request):
    try:
        payments = Order.objects.filter(user_id=request.user.id).order_by('-id')[:5]
        ads = Advertisement.objects.order_by('id')
        total_refs = ReferralSys.objects.filter(id_referrer=request.user.id).order_by('-id')
    finally:
        paginator = Paginator(total_refs, 5)
        page = request.GET.get('referrals')
        refs = paginator.get_page(page)
    d = {'payments': payments, 'ads': ads, 'refs': refs}
    return render(request, 'main/main_page.html', {"d": d})

@login_required
def panel_stats(request):
    try:
        main_stats = Statistic.objects.latest('id')
        last_order = Order.objects.filter(status=True).latest('id')
        last_withdraw = Transfer.objects.filter(status=1).latest('id')
        top5_orders = Order.objects.filter(status=True).order_by('-amount')[:10]
        top5_wds = Transfer.objects.filter(status=1).order_by('-amount')[:10]
    except ObjectDoesNotExist:
        top5_orders = top5_wds = main_stats = users_count = last_order = last_withdraw = 0
    else:
        users_count = Profile.objects.latest('id')
    finally:
        d = {'stats': main_stats, 'u_count': users_count, 'last_o': last_order, 'last_wd': last_withdraw, 'top5_ords': top5_orders, 'top5_wds': top5_wds}
        return render(request, 'main/statistic.html', {"d": d})

@login_required
def shop(request):
    factories = Factory.objects.order_by('id')[:6]
    towers = Tower.objects.order_by('id')[:6]
    return render(request, 'main/shop.html', {'factories': factories, 'towers': towers})

@login_required
def inventory(request):
    towers = ClientTower.objects.filter(user_id=request.user.id)
    factories = ClientFactory.objects.filter(user_id=request.user.id)
    levels = TowerLevel.objects.all()
    return render(request, 'main/inventory.html', {'towers': towers, 'factories': factories, 'levels': levels})

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
                client.oil -= convert
                client.balance += user_request
                client.save()
                messages.add_message(request, messages.SUCCESS, "Операция успешно выполнена. Зачислено: " + str(user_request) + " руб.")
        else:
            messages.add_message(request, messages.ERROR, "Введено неверное значение. Действие отменено.")
    return render(request, 'main/exchanger.html', {'made': client_rubs()})

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
                check = ClientFactory.objects.get(user_id=client.id, factory__tower_id=good.id)
                data = ClientTower(tower=good, user_id=client.id, work=timed())
                data.save()
                client.balance -= good.price
                client.stat_tower += 1 # user stat
                client.save()
                # Statistic global
                stat = Statistic.objects.latest('id')
                stat.tower += 1
                stat.save()
                messages.add_message(request, messages.SUCCESS, "Вы успешно приобрели товар.")
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, "Для покупки этой башни необходимо купить завод этого же типа.")
    elif category == "1":
        # if category - Factory
        good = get_object_or_404(Factory, id=goods)
        if client.balance < good.price:
            messages.add_message(request, messages.ERROR, "У вас нет необходимой суммы для оплаты товара.")
        else:
            try:
                check = ClientFactory.objects.get(user_id=client.id, factory=good)
                messages.add_message(request, messages.WARNING, "Этот завод у вас уже приобретен.")
            except ObjectDoesNotExist:
                data = ClientFactory(factory=good, user_id=client.id)
                data.save()
                client.balance -= good.price
                client.save()
                messages.add_message(request, messages.SUCCESS, "Вы успешно приобрели товар.")
    return redirect('shop')

@login_required
def get_all_oil(request):
    timed = lambda: int(round(time.time()))
    towers = ClientTower.objects.filter(user_id=request.user.id)
    if towers:
        oil_counter = 0
        levels = TowerLevel.objects.all()
        for tower in towers:
            if timed() - tower.work >= 0:
                tower.work = timed() + 86400
                tower.save()
                if tower.level != 1:
                    oil_counter += levels[tower.level - 1].up
                oil_counter += tower.tower.oil
        if oil_counter > 0:
            client = Profile.objects.get(user_id=request.user.id)
            client.oil += oil_counter
            client.stat_produced += oil_counter
            client.save()
            stat = Statistic.objects.latest('id')
            stat.oil += oil_counter
            stat.save()
            messages.add_message(request, messages.SUCCESS, "Вы собрали нефть с ожидающих вышек. Всего зачислено нефти: {0} единиц.".format(oil_counter))
        else:
            messages.add_message(request, messages.WARNING, "В данный момент у вас нет вышек, с которых можно собрать нефть. Пожалуйста, попробуйте позже.")
    return redirect('inventory')

@login_required
def tower_level_up(request, pk):
    try:
        tower = ClientTower.objects.get(user_id=request.user.id, pk=pk)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Данная вышка не зарегистрирована на ваш аккаунт.")
        return redirect('inventory')
    if tower.level == 16:
        messages.add_message(request, messages.WARNING, "Эта вышка имеет максимальный уровень.")
        return redirect('inventory')
    client = Profile.objects.get(user_id=request.user.id)
    levels = TowerLevel.objects.all()
    if client.balance >= levels[tower.level].price:
        client.balance -= levels[tower.level].price
        client.save()
        tower.level += 1
        tower.save()
        messages.add_message(request, messages.SUCCESS, "Вы успешно приобрели повышение уровня для нефтяной вышки.")
    else:
        messages.add_message(request, messages.WARNING, "Вы не имеете необходимой суммы для оплаты услуги.")
    return redirect('inventory')