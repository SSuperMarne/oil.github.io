from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Order, Promotion
from .forms import ReplenishForm
from client.models import Profile, ReferralSys
from game.models import Statistic
import base64
import hashlib

"""
Configuration of payment systems
"""
FREEKASSA_SHOP_ID = "70935"
FREEKASSA_SECRET = "332bwjy1"
PAYEER_SHOP_ID = "518803834"
PAYEER_CURR = "RUB"
PAYEER_SECRET = "Qt8rv6hCT379QQduzSJnCVBC3WePv3pT"

"""
Sub-functions for payments
"""
def add_balance(order, success):
    client = Profile.objects.get(user_id=order.user_id)
    client.balance += order.amount  # add balance
    client.stat_pay += order.amount  # add stat
    client.save()
    order.status = True
    order.save()
    # Statistic
    s = Statistic.objects.get(id=1)
    s.donated += order.amount
    s.save()
    # ReferralSystem
    try:
        r = ReferralSys.objects.get(id_referral=order.user_id)
    except ObjectDoesNotExist:
        return HttpResponse(str(success))
    r.profit += order.amount
    r.save()
    r_referrer = Profile.objects.get(user_id=r.id_referrer)
    r_referrer.balance += order.amount / 10
    r_referrer.save()
    return HttpResponse(str(success))

def create_pay_sign(request, amount, system, m_orderid):
    description = "Пополнение баланса пользователя %s" % request.user.username
    # Free-Kassa
    if system == "1":
        list_for_sign = map(str, [FREEKASSA_SHOP_ID, amount, FREEKASSA_SECRET, m_orderid])
        result_string = ":".join(list_for_sign).encode()
        sign_hash = hashlib.md5(result_string)
        sign = sign_hash.hexdigest()
        return redirect("https://www.free-kassa.ru/merchant/cash.php?m={0}&oa={1}&o={2}&s={3}&em={4}".format(FREEKASSA_SHOP_ID, amount, m_orderid, sign, request.user.email))
    # Payeer
    elif system == "2":
        m_desc = base64.b64encode(description.encode('utf-8')).decode('utf-8')
        m_amount = str(amount) + ".00" # требование Payeer
        list_of_value_for_sign = map(str, [PAYEER_SHOP_ID, m_orderid, m_amount, PAYEER_CURR, m_desc, PAYEER_SECRET])
        result_string = ":".join(list_of_value_for_sign).encode()
        sign_hash = hashlib.sha256(result_string)
        sign = sign_hash.hexdigest().upper()
        context = [{'m_shop': PAYEER_SHOP_ID, 'm_orderid': m_orderid, 'm_amount': m_amount, 'm_curr': PAYEER_CURR, 'm_desc': m_desc, 'm_sign': sign}]
        return render(request, 'payment/process_payeer.html', {'context': context})

def promo_check(order):
    try:
        promotion = Promotion.objects.latest('id')
    except ObjectDoesNotExist:
        promotion = 0
    if promotion != 0:
        promo = order.amount * promotion.promo / 100
        order.amount += round(promo)
        order.save()

"""
Other payments function
"""
@login_required
def add_payment(request):
    try:
        promotion = Promotion.objects.latest('id')
    except ObjectDoesNotExist:
        promotion = 0
    if request.method == 'POST':
        form = ReplenishForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            system = form.cleaned_data.get('system')
            # Создание платежа
            order = Order(amount=amount, user_id=request.user.id, status=False)
            order.save()
            return create_pay_sign(request, amount, system, order.id)
        else:
            messages.add_message(request, messages.ERROR, "Введено неверное значение. Действие отменено.")
    return render(request, 'main/add_payment.html', {'promo': promotion})

@csrf_exempt
def payeer_status(request):
    if request.method == 'POST' and 'm_operation_id' in request.POST and 'm_sign' in request.POST:
        list_of_value_for_sign = map(str, [request.POST['m_operation_id'], request.POST['m_operation_ps'], 
        request.POST['m_operation_date'], request.POST['m_operation_pay_date'], request.POST['m_shop'], 
        request.POST['m_orderid'], request.POST['m_amount'], request.POST['m_curr'], 
        request.POST['m_desc'], request.POST['m_status'], PAYEER_SECRET])
        result_string = ":".join(list_of_value_for_sign).encode()
        sign_hash = hashlib.sha256(result_string)
        sign = sign_hash.hexdigest().upper()
        if request.POST['m_sign'] == sign and request.POST['m_status'] == "success":
            success = request.POST['m_orderid'] + ".|success"
            order = Order.objects.get(id=request.POST['m_orderid'])
            promo_check(order)
            return add_balance(order, success)
        if request.POST['m_sign'] == sign and request.POST['m_status'] == "fail":
            fail = request.POST['m_orderid'] + ".|fail"
            return HttpResponse(str(fail))
    else:
        return redirect('landing_main')

@csrf_exempt
def fk_status(request):
    if request.method == 'POST' and 'MERCHANT_ORDER_ID' in request.POST:
        list_for_sign = map(str, [FREEKASSA_SHOP_ID, request.POST['AMOUNT'], FREEKASSA_SECRET, request.POST['MERCHANT_ORDER_ID']])
        result_string = ":".join(list_for_sign).encode()
        sign_hash = hashlib.md5(result_string)
        sign = sign_hash.hexdigest()
        if request.POST['SIGN'] == sign:
            success = "YES"
            order = Order.objects.get(id=request.POST['MERCHANT_ORDER_ID'])
            promo_check(order)
            return add_balance(order, success)
    else:
        return redirect('landing_main')

def payment_status(request, status):
    if status == "success":
        messages.add_message(request, messages.INFO, "Оплата была успешно завершена. Спасибо за покупку.")
    else:
        messages.add_message(request, messages.INFO, "Ошибка в проведении платежа. Платеж отменён.")
    return redirect('payment')