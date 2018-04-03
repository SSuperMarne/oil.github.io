from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from .forms import SignUpForm, TransferForm
from .models import Profile, Transfer, ReferralSys
from payment.views import create_pay_sign
from payment.models import Order

"""
Registration
"""
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            ref = int(form.cleaned_data.get('ref'))
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # ReferralSystem
            if ref != 0:
                try:
                    referrer_check = Profile.objects.get(user_id=ref)
                except ObjectDoesNotExist:
                    return redirect('panel_main')
                ref_create = ReferralSys(id_referral=user.id, id_referrer=ref, profit=0)
                ref_create.save()
            return redirect('panel_main')
    else:
        form = SignUpForm()
    try:
        referrer = request.session['ref']
    except KeyError:
        referrer = 0
    return render(request, 'registration/registration.html', {'form': form, 'ref': referrer})

def referral(request, referrer):
    request.session['ref'] = referrer
    return redirect('landing_main')

"""
User profiles
"""
@login_required
def u_profile(request):
    ref_profit = ReferralSys.objects.filter(id_referrer=request.user.id).aggregate(value=Sum('profit'))
    return render(request, 'main/profile.html', {'ref_profit': ref_profit})

"""
The function for withdraw
"""
@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        client = Profile.objects.get(user_id=request.user.id)
        if form.is_valid() and client.stat_pay >= 10 and client.stat_produced >= 500:
            money = form.cleaned_data.get('rubs')
            if money <= client.balance:  
                transfer = Transfer(amount=money, system=form.cleaned_data.get('system'), 
                vault=form.cleaned_data.get('vault'), user_id=request.user.id, status=3)
                transfer.save()
                client.balance = client.balance - money
                client.save()
                messages.add_message(request, messages.INFO, "Заявка на вывод поставлена в очередь")
            else:
                messages.add_message(request, messages.ERROR, "Недостаточно средств на балансе аккаунта")
        else:
            messages.add_message(request, messages.ERROR, "Для вывода средств необходимо пополнить баланс минимум на 10 рублей, а также добыть 500 ед. нефти.")
    history = Transfer.objects.order_by('-id').filter(user_id=request.user.id)[:10]
    return render(request, 'main/transfer.html', {'history': history})

"""
Management of customers payments
"""
@login_required
def payment_manage(request, pk, action):
    try:
        check_payment = Order.objects.get(pk=pk, user_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Платеж не найден.")
        return redirect('payment_history')
    else:
        if action == "pay":
            return create_pay_sign(request, check_payment.amount, "1", check_payment.id)
        if action == "rm":
            if check_payment.status:
                messages.add_message(request, messages.SUCCESS, "Платёж #{} успешно удален из вашей истории платежей.".format(check_payment.id))
                check_payment.delete()
            else:
                messages.add_message(request, messages.WARNING, "Мы не можем удалить этот платеж. Он ещё не был оплачен.")
        return redirect('payment_history')

@login_required
def payment_history(request):
    payments = Order.objects.order_by('-id').filter(user_id=request.user.id)
    return render(request, 'main/history.html', {'payments': payments})