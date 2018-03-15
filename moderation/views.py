from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from game.models import Support, Statistic
from client.models import Transfer
from .forms import ModForm

@login_required
def moderation(request):
    # Статусы платежей: 1 - выплачено, 2 - отклонено, 3 - обработка
    if request.user.is_staff:
        if request.method == 'POST':
            form = ModForm(request.POST)
            if form.is_valid():
                nickname = form.cleaned_data.get('nickname')
                oil = form.cleaned_data.get('oil')
                rub = form.cleaned_data.get('rub')
                user = get_object_or_404(User, username=nickname)
                old_oil = user.profile.oil
                old_rub = user.profile.balance
                user.profile.oil = user.profile.oil + oil
                user.profile.balance = user.profile.balance + rub
                user.save()
                messages.add_message(request, messages.INFO, "Значения успешно изменены. Нефть (было): {0}, стало: {1}. Рубль (было): {2}, стало: {3}.".format(old_oil, 
                    user.profile.oil, old_rub, user.profile.balance))
            else:
                messages.add_message(request, messages.ERROR, "ОШИБКА: В форме допущены ошибки. Убедитесь, что заполнены все поля. Укажите 0, если вы не хотите менять параметр.")
        draws = Transfer.objects.all().order_by('-id')
        tickets = Support.objects.all().order_by('-id')
        return render(request, 'mod/moderator.html', {'draws': draws, 'tickets': tickets})
    else:
        raise PermissionDenied

@login_required
def support_del(request, pk):
    if request.user.is_staff:
        a = get_object_or_404(Support, pk=pk)
        a.delete()
        messages.add_message(request, messages.INFO, "Действие успешно выполнено")
        return redirect('moderation')
    else:
        raise PermissionDenied

@login_required
def transfer_change(request, status, pk):
    if request.user.is_staff:
        transfer = get_object_or_404(Transfer, pk=pk)
        if status == "accept":
            transfer.status = 1
            transfer.save()
            # Statistic global
            stat = Statistic.objects.get(id=1)
            stat.exchanged = stat.exchanged + transfer.amount
            stat.save()
            # Statistic user
            client = User.objects.get(id=transfer.user_id)
            client.profile.stat_payout = client.profile.stat_payout + transfer.amount
            client.save()
            messages.add_message(request, messages.INFO, "Статус заявки успешно изменен")
        else:
            transfer.status = 2
            transfer.save()
            # Back to client balance
            client = User.objects.get(id=transfer.user_id)
            client.profile.balance = client.profile.balance + transfer.amount
            client.save()
            messages.add_message(request, messages.INFO, "Статус заявки успешно изменен. Деньги возвращены на баланс клиента.")
        return redirect('moderation')
    else:
        raise PermissionDenied