from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Transfer
from .forms import ExchangeForm, ReplenishForm, TransferForm
import math
import base64
import hashlib

@login_required
def add_payment(request):
    if request.method == 'POST':
        form = ReplenishForm(request.POST)
        if form.is_valid():
            m_amount = form.cleaned_data.get('m_amount')
            description = form.cleaned_data.get('m_desc')
            m_shop = "0000000" # ID магазина
            m_curr = "RUB" # валюта
            m_desc = base64.b64encode(description.encode('utf-8')).decode('utf-8')
            m_key = "secret_key" # секретный ключ
            order = Order(amount=m_amount, user_id=request.user.id, status=False)
            order.save()
            m_orderid = order.id
            # требование Payeer добавлять .00 у суммы
            m_amount = str(form.cleaned_data.get('m_amount')) + ".00"
            # создание подписи #
            list_of_value_for_sign = map(str, [m_shop, m_orderid, m_amount, m_curr, m_desc, m_key])
            result_string = ":".join(list_of_value_for_sign).encode()
            sign_hash = hashlib.sha256(result_string)
            sign = sign_hash.hexdigest().upper()
            # конец создания подписи #
            context = [{'m_shop': m_shop, 'm_orderid': m_orderid, 'm_amount': m_amount, 'm_curr': m_curr, 'm_desc': m_desc, 'm_sign': sign}]
            return render(request, 'payment/process.html', {'context': context})
        else:
            messages.add_message(request, messages.ERROR, "Введено неверное значение. Действие отменено.")
            return redirect('replenish')
    else:
        return render(request, 'main/add_payment.html')