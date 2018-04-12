from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import Ticket, PersonalMessage
from .forms import NewPMForm, AddPMForm

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
            pm = PersonalMessage(ticket=ticket, message=text, status=True)
            pm.save()
            messages.add_message(request, messages.SUCCESS, "Сообщение успешно отправлено!")
            return redirect('pm_list')
    else:
        form = NewPMForm()
    return render(request, 'pm/pm_new_create.html', {"form": form})

@login_required
def pm_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.owner != request.user and ticket.recipient != request.user.id:
        messages.add_message(request, messages.WARNING, "Нет прав!")
        return redirect('pm_list')
    if request.method == 'POST':
        form = AddPMForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            if ticket.owner == request.user:
                pm = PersonalMessage(ticket=ticket, message=text, status=True)
            else:
                pm = PersonalMessage(ticket=ticket, message=text, status=False)
            pm.save()
            messages.add_message(request, messages.SUCCESS, "Сообщение успешно отправлено!")
            return redirect('pm_view', pk=pk)
    else:
        pm = PersonalMessage.objects.filter(ticket=ticket)
        return render(request, 'pm/pm_view.html', {"ticket": ticket, "pms": pm})

@login_required
def pm_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.owner == request.user or ticket.recipient == request.user.id:
        ticket.delete()
        messages.add_message(request, messages.SUCCESS, "Диалог был успешно удален!")
    else:
        messages.add_message(request, messages.WARNING, "Нет прав!")
    return redirect('pm_list')