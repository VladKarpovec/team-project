from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Event
from .forms import EventForm
import calendar
from datetime import date

@login_required
def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


@staff_member_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events:event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


@staff_member_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events:event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})


@staff_member_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('events:event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})




@login_required
def event_calendar(request, year=None, month=None):
    today = date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month

    cal = calendar.Calendar()
    month_days = cal.monthdatescalendar(year, month)

    events = Event.objects.filter(date__year=year, date__month=month)
    events_map = {}
    for event in events:
        events_map.setdefault(event.date, []).append(event)

    weeks = []
    for week in month_days:
        week_data = []
        for day in week:
            week_data.append({
                'date': day,
                'events': events_map.get(day, [])
            })
        weeks.append(week_data)

    context = {
        "weeks": weeks,
        "month_name": calendar.month_name[month],
        "year": year,
        "month": month,
        "today": today
    }
    return render(request, "events/event_calendar.html", context)

