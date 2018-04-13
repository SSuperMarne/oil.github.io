from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Q
from .models import Ticket, PersonalMessage
from .forms import NewPMForm, AddPMForm, AddSupportForm, ReplySupportForm

"""
Sub-functions for personal messages
"""
def ticket_create(request, recipient, title, text, status):
    ticket = Ticket(owner=request.user, recipient=recipient, title=title, status=status)
    ticket.save()
    pm = PersonalMessage(ticket=ticket, message=text, status=True)
    pm.save()
    return True

"""
Main functions
"""
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
            if ticket_create(request, recipient.id, title, text, 0):
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
        if ticket.status == 1:
            messages.add_message(request, messages.ERROR, "Этот тикет закрыт. Ответы в закрытый тикет невозможны.")
            return redirect('pm_list')
        form = AddPMForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            if ticket.status == 2: # смена статуса на "ожидание", если тикет открыт
                ticket.status = 3
                ticket.save()
            if ticket.owner == request.user: # от чьего имени отправляется сообщение
                pm = PersonalMessage(ticket=ticket, message=text, status=True)
            else:
                pm = PersonalMessage(ticket=ticket, message=text, status=False)
            pm.save()
            messages.add_message(request, messages.SUCCESS, "Сообщение успешно отправлено!")
            return redirect('pm_view', pk=pk)
    else:
        form = AddPMForm()
        pm = PersonalMessage.objects.filter(ticket=ticket)
        return render(request, 'pm/pm_view.html', {"ticket": ticket, "pms": pm, "form": form})

@login_required
def pm_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.owner == request.user or ticket.recipient == request.user.id:
        ticket.delete()
        messages.add_message(request, messages.SUCCESS, "Диалог был успешно удален!")
    else:
        messages.add_message(request, messages.WARNING, "Нет прав!")
    return redirect('pm_list')

"""
Technical support functions
"""
@login_required
def pm_support_new(request):
    if request.method == 'POST':
        form = AddSupportForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            if ticket_create(request, 0, "Запрос в техническую поддержку", text, 3):
                messages.add_message(request, messages.SUCCESS, "Запрос в техническую поддержку был успешно создан!")
                return redirect('pm_list')
    else:
        form = AddSupportForm()
    return render(request, 'pm/support.html', {"form": form})

@login_required
def pm_support_view(request, pk):
    if request.user.is_staff:
        ticket = get_object_or_404(Ticket, pk=pk)
        pm = PersonalMessage.objects.filter(ticket=ticket)
        if request.method == 'POST':
            form = ReplySupportForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('text')
                close = form.cleaned_data.get('close')
                if close: # если чекбокс отмечен закрыть тикет
                    ticket.status = 1
                    ticket.save()
                else:
                    ticket.status = 2
                    ticket.save()
                pm_create = PersonalMessage(ticket=ticket, message=text, status=False)
                pm_create.save()
                messages.add_message(request, messages.SUCCESS, "Сообщение успешно отправлено!")
        return render(request, 'moderation/pm_view.html', {"ticket": ticket, "pms": pm})
    else:
        raise PermissionDenied