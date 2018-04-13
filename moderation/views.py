from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from game.models import Statistic, ClientTower, ClientFactory
from client.models import Profile, Transfer, ReferralSys
from pm.models import Ticket
from payment.views import autopay
from .forms import ModifyForm, NicknameForm

"""
Sub-functions for moderation
"""
def success_withdraw(transfer, client):
    transfer.status = 1
    transfer.save()
    # Statistic global
    stat = Statistic.objects.latest('id')
    stat.exchanged += transfer.amount
    stat.save()
    # Statistic user
    client.profile.stat_payout += transfer.amount
    client.save()

"""
Main functions
"""
@login_required
def moderation(request):
    if request.user.is_staff:
        total_draws = Transfer.objects.all().order_by('-id')
        tickets = Ticket.objects.filter(status=3).order_by('-id')
        paginator = Paginator(total_draws, 10)
        page = request.GET.get('draws')
        draws = paginator.get_page(page)
        return render(request, 'mod/moderator.html', {'draws': draws, 'tickets': tickets})
    else:
        raise PermissionDenied

@login_required
def mod_actions(request, action):
    form_not_valid = lambda: messages.add_message(request, messages.ERROR, "ОШИБКА: В форме допущены ошибки. Убедитесь, что заполнены все поля.")
    if request.user.is_staff and request.method == 'POST':
        if action == "referrals":
            form = NicknameForm(request.POST)
            if form.is_valid():
                user = get_object_or_404(User, username=form.cleaned_data.get('nickname'))
                total_profit = ReferralSys.objects.filter(id_referrer=user.id).aggregate(value=Sum('profit'))
                referrals = ReferralSys.objects.filter(id_referrer=user.id)
                return render(request, 'mod/mod_reflist.html', {'total_profit': total_profit, 'referrals': referrals})
            else:
                form_not_valid()
        if action == "statistic":
            form = NicknameForm(request.POST)
            if form.is_valid():
                user = get_object_or_404(User, username=form.cleaned_data.get('nickname'))
                profile = Profile.objects.get(pk=user.id)
                d = {'info': user, 'statistic': profile}
                return render(request, 'mod/mod_userinfo.html', {'d': d})
            else:
                form_not_valid()
        if action == "inventory":
            form = NicknameForm(request.POST)
            if form.is_valid():
                user = get_object_or_404(User, username=form.cleaned_data.get('nickname'))
                factories = ClientFactory.objects.filter(user_id=user.id)
                towers = ClientTower.objects.filter(user_id=user.id)
                total_oil = count_towers = 0
                if towers:
                    for tower in towers:
                        count_towers += 1
                        total_oil += tower.tower_oil
                d = {'info': user, 'factories': factories, 'towers': towers, 'total_oil': total_oil, 'count_towers': count_towers}
                return render(request, 'mod/mod_inventory.html', {'d': d})
            else:
                form_not_valid()
        if action == "modify":
            form = ModifyForm(request.POST)
            if form.is_valid():
                nickname = form.cleaned_data.get('nickname')
                oil = form.cleaned_data.get('oil')
                rub = form.cleaned_data.get('rub')
                user = get_object_or_404(User, username=nickname)
                old_oil = user.profile.oil
                old_rub = user.profile.balance
                user.profile.oil += oil
                user.profile.balance += rub
                user.save()
                messages.add_message(request, messages.SUCCESS, "Значения успешно изменены. Нефть (было): {0}, стало: {1}. Рубль (было): {2}, стало: {3}.".format(old_oil, 
                    user.profile.oil, old_rub, user.profile.balance))
            else:
                form_not_valid()
        return redirect('moderation')
    else:
        raise PermissionDenied

@login_required
def transfer_change(request, status, pk):
    if request.user.is_staff:
        transfer = get_object_or_404(Transfer, pk=pk)
        client = User.objects.get(id=transfer.user_id)
        if status == "accept":
            success_withdraw(transfer, client)
            messages.add_message(request, messages.SUCCESS, "Статус заявки успешно изменен.")
        else:
            transfer.status = 2
            transfer.save()
            # Back to client balance
            client.profile.balance += transfer.amount
            client.save()
            messages.add_message(request, messages.SUCCESS, "Статус заявки успешно изменен. Деньги возвращены на баланс клиента.")
        return redirect('moderation')
    else:
        raise PermissionDenied

@login_required
def transfer_auto(request, pk):
    if request.user.is_staff:
        transfer = get_object_or_404(Transfer, pk=pk)
        if transfer.system == "1":
            client = User.objects.get(id=transfer.user_id)
            auto = autopay(transfer)
            if auto == True:
                success_withdraw(transfer, client)
                messages.add_message(request, messages.SUCCESS, "Выплата средств успешно произведена, а статус заявки был изменен.")
            else:
                messages.add_message(request, messages.ERROR, auto)
        else:
            messages.add_message(request, messages.ERROR, "В платеже указана недопустимая система для автовывода.")
        return redirect('moderation')
    else:
        raise PermissionDenied