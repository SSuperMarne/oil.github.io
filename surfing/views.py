from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tariff, SurfingSite
from .forms import AddSurfForm

def surfing_add(request):
    tariffs = Tariff.objects.all()
    sites = SurfingSite.objects.filter(user_id=request.user.id)
    if request.method == "POST":
        form = AddSurfForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            url = form.cleaned_data.get('url')
            tariff = form.cleaned_data.get('tariff')
            if request.user.profile.stat_pay < 50:
                messages.add_message(request, messages.WARNING, "Вам необходимо пополнить счет как минимум на 50 рублей для покупки рекламы.")
                return redirect('add_surfing')
            if request.user.profile.balance < tariff.price:
                messages.add_message(request, messages.WARNING, "У вас недостаточно средств на балансе для оплаты услуги.")
                return redirect('add_surfing')
            add = SurfingSite(tariff=tariff, user_id=request.user.id, balance=tariff.price, title=title, url=url, status=True)
            add.save()
            request.user.profile.balance -= tariff.price
            request.user.save()
            messages.add_message(request, messages.SUCCESS, "Сайт успешно добавлен, первый взнос внесен. Активируйте сайт для начала показа.")
    else:
        form = AddSurfForm()
    return render(request, 'surfing/add_site.html', {'tariffs': tariffs, 'form': form, 'sites': sites})