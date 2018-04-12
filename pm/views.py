from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import Ticket, PersonalMessage
from .forms import NewPMForm

@login_required
def pm_list(request):
    pm = Ticket.objects.filter(Q(owner_id=request.user.id) | Q(recipient=request.user.id)).order_by('-id')
    return render(request, 'pm/pm_list.html', {"pm": pm})

@login_required
def pm_new_create(request):
    if request.method == 'POST':
        form = NewPMForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            title = form.cleaned_data.get('title')
            text = form.cleaned_data.get('text')
            try:
                recipient = User.objects.get(username=username)
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, "Пользователь с данным логином не существует.")
                return redirect('pm_new_create')
            ticket = Ticket(owner=request.user, recipient=recipient.id, title=title)
            ticket.save()
            pm = PersonalMessage(ticket=ticket, message=text)
            pm.save()
            messages.add_message(request, messages.SUCCESS, "Сообщение успешно отправлено!")
            return redirect('pm_list')
    else:
        form = NewPMForm()
    return render(request, 'pm/pm_new_create.html', {"form": form})