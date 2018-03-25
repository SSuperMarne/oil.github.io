from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Order
from .forms import ReplenishForm
from client.models import Profile, ReferralSys
from game.models import Statistic
import base64
import hashlib

# configuration
PAYEER_SHOP_ID = "518803834"
PAYEER_CURR = "RUB"
PAYEER_SECRET = "Qt8rv6hCT379QQduzSJnCVBC3WePv3pT"

@login_required
def add_payment(request):
    if request.method == 'POST':
        form = ReplenishForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            system = form.cleaned_data.get('system')
            description = "Пополнение баланса пользователя %s" % request.user.username
            # Free-Kassa
            if system == "1":
                pass
            # Payeer
            elif system == "2":
                m_desc = base64.b64encode(description.encode('utf-8')).decode('utf-8')
                order = Order(amount=amount, user_id=request.user.id, status=False)
                order.save()
                m_orderid = order.id
                # требование Payeer добавлять .00 у суммы
                m_amount = str(amount) + ".00"
                # создание подписи #
                list_of_value_for_sign = map(str, [PAYEER_SHOP_ID, m_orderid, m_amount, PAYEER_CURR, m_desc, PAYEER_SECRET])
                result_string = ":".join(list_of_value_for_sign).encode()
                sign_hash = hashlib.sha256(result_string)
                sign = sign_hash.hexdigest().upper()
                # конец создания подписи #
                context = [{'m_shop': PAYEER_SHOP_ID, 'm_orderid': m_orderid, 'm_amount': m_amount, 'm_curr': PAYEER_CURR, 'm_desc': m_desc, 'm_sign': sign}]
                return render(request, 'payment/process_payeer.html', {'context': context})
        else:
            messages.add_message(request, messages.ERROR, "Введено неверное значение. Действие отменено.")
    return render(request, 'main/add_payment.html')

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
            client = Profile.objects.get(user_id=order.user_id)
            client.balance = client.balance + order.amount  # add balance
            client.stat_pay = client.stat_pay + order.amount  # add stat
            client.save()
            order.status = True
            order.save()
            # statistics
            s = Statistic.objects.get(id=1)
            s.donated = s.donated + order.amount
            s.save()
            # ReferralSys
            try:
                r = ReferralSys.objects.get(id_referral=order.user_id)
            except ObjectDoesNotExist:
                return HttpResponse(str(success))
            r.profit = r.profit + order.amount
            r.save()
            r_referrer = Profile.objects.get(user_id=r.id_referrer)
            r_referrer.balance = r_referrer.balance + order.amount / 10
            r_referrer.save()
            return HttpResponse(str(success))
        if request.POST['m_sign'] == sign and request.POST['m_status'] == "fail":
            fail = request.POST['m_orderid'] + ".|fail"
            return HttpResponse(str(fail))
    else:
        return redirect('landing_main')

def payment_status(request, status):
    if status == "success":
        messages.add_message(request, messages.INFO, "Оплата была успешно завершена. Спасибо за покупку.")
    else:
        messages.add_message(request, messages.INFO, "Ошибка в проведении платежа. Платеж отменён.")
    return redirect('payment')