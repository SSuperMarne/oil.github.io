from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
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
    return redirect('register')

"""
User profiles
"""
@login_required
def u_profile(request):
    return render(request, 'main/profile.html')

"""
The function for withdraw
"""
@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        client = Profile.objects.get(user_id=request.user.id)
        if form.is_valid() and client.stat_pay >= 10 and client.stat_produced >= 50:
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
            messages.add_message(request, messages.ERROR, "Для вывода средств необходимо пополнить баланс минимум на 10 рублей, а также добыть 50 ед. нефти.")
    history = Transfer.objects.order_by('-id').filter(user_id=request.user.id)[:10]
    return render(request, 'main/transfer.html', {'history': history})

"""
Management of customers payments
"""
@login_required
def supplement(request, order):
    try:
        check_payment = Order.objects.get(pk=order, user_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Платеж не найден.")
        return redirect('payment_history')
    else:
        return create_pay_sign(request, check_payment.amount, "1", check_payment.id)

@login_required
def payment_delete(request, order):
    try:
        check_payment = Order.objects.get(pk=order, user_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Платеж не найден.")
    else:
        check_payment.delete()
        messages.add_message(request, messages.SUCCESS, "Действие успешно выполнено.")
    return redirect('payment_history')

@login_required
def payment_history(request):
    payments = Order.objects.order_by('-id').filter(user_id=request.user.id)
    return render(request, 'main/history.html', {'payments': payments})