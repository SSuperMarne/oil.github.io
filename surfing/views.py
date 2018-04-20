from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Tariff, SurfingSite, SurfingHistory
from .forms import AddSurfForm, EditSurfForm
import time
import json

@login_required
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
            messages.add_message(request, messages.SUCCESS, "Сайт успешно добавлен и активирован, первый взнос внесен.")
    else:
        form = AddSurfForm()
    return render(request, 'surfing/add_site.html', {'tariffs': tariffs, 'form': form, 'sites': sites})

@login_required
def surfing_edit(request, pk):
    try:
        site = SurfingSite.objects.get(pk=pk, user_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Нет прав!")
        return redirect('add_surfing')
    tariffs = Tariff.objects.all()
    if request.method == "POST":
        form = EditSurfForm(request.POST)
        if form.is_valid():
            balance = form.cleaned_data.get('balance')
            if balance > round(site.balance):
                difference = balance - round(site.balance)
                if request.user.profile.balance < difference:
                    messages.add_message(request, messages.WARNING, "У вас недостаточно средств на балансе для повышения баланса сайта.")
                else:
                    request.user.profile.balance -= difference
                    request.user.save()
                    site.balance += difference
                    messages.add_message(request, messages.SUCCESS, "{} руб. было зачислено на баланс сайта. Средства списаны с вашего баланса.".format(difference))
            site.url = form.cleaned_data.get('url')
            site.title = form.cleaned_data.get('title')
            site.tariff = form.cleaned_data.get('tariff')
            site.status = form.cleaned_data.get('status')
            site.save()
            messages.add_message(request, messages.SUCCESS, "Информация о сайте была обновлена.")
            return redirect('add_surfing')
    return render(request, 'surfing/edit_site.html', {'tariffs': tariffs, 'site': site})

@login_required
def surfing_list(request):
    sites = SurfingSite.objects.filter(status=True).order_by('-id')
    return render(request, 'surfing/surfing_list.html', {'sites': sites})

@login_required
def surfing(request, pk):
    try:
        site = SurfingSite.objects.get(pk=pk, status=True)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Такого сайта не существует")
        return redirect('list_surfing')
    request.session['surfingend'] = round(time.time()) + site.tariff.time
    return render(request, 'surfing/surfing.html', {'site': site})

@login_required
def status(request):
    if request.is_ajax():
        if request.method == "POST":
            try:
                data = json.loads(request.body.decode("utf-8"))
                site_id = data['id']
            except ValueError:
                return HttpResponseBadRequest() # Not JSON

            try:
                site = SurfingSite.objects.get(pk=site_id, status=True)
            except ObjectDoesNotExist:
                return HttpResponseBadRequest() # Bad ID

            try:
                check = SurfingHistory.objects.get(user=request.user, site=site)
            except ObjectDoesNotExist:
                pass
            else:
                return HttpResponseBadRequest("Вы уже просматривали этот сайт.")

            price_for_one = site.tariff.price / 1000
            if price_for_one > site.balance:
                return HttpResponseBadRequest("Сайт не имеет средств на балансе.")
            diff = request.session.get('surfingend', 9 ** 10) - round(time.time())
            if diff > 0:
                return HttpResponseBadRequest("Прошло недостаточно времени.")

            request.user.profile.balance += price_for_one
            request.user.save()
            site.balance -= price_for_one
            site.save()
            check_add = SurfingHistory(user=request.user, site=site)
            check_add.save()
            return HttpResponse("OK")
        return HttpResponseBadRequest() # Unknown AJAX request
    else:
        return redirect('landing_main')