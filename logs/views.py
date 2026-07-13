from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Log, Entry
from .forms import LogForm, EntryForm
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
import json


@login_required
def logs(request):
    logs = Log.objects.filter(owner=request.user)

    context = {"logs": logs}
    return render(request, "logs/logs.html", context)


@login_required
def log(request, log_id):

    log = get_object_or_404(
        Log,
        id=log_id,
        owner=request.user,
    )

    entries = log.entries.all()

    context = {
        "log": log,
        "entries": entries,
    }

    return render(
        request,
        "logs/log.html",
        context,
    )


@login_required
def new_log(request):

    if request.method != "POST":
        form = LogForm()

    else:
        form = LogForm(request.POST)

        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.owner = request.user
            new_log.save()
            return redirect("logs")

    return render(
        request,
        "logs/new_log.html",
        {"form": form},
    )

@login_required
def new_entry(request, log_id):

    log = get_object_or_404(
        Log,
        id=log_id,
        owner=request.user,
    )

    if request.method != "POST":
        form = EntryForm()

    else:
        form = EntryForm(request.POST)

        if form.is_valid():
            entry = form.save(commit=False)
            entry.log = log
            entry.save()

            return redirect("log", log_id=log.id)

    context = {
        "log": log,
        "form": form,
    }

    return render(
        request,
        "logs/new_entry.html",
        context,
    )

@login_required
def edit_entry(request, entry_id):

    entry = get_object_or_404(
        Entry,
        id=entry_id,
    )

    # امنیت
    if entry.log.owner != request.user:
        return redirect("logs")

    if request.method != "POST":
        form = EntryForm(instance=entry)

    else:
        form = EntryForm(
            request.POST,
            instance=entry,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "log",
                log_id=entry.log.id,
            )

    context = {
        "entry": entry,
        "log": entry.log,
        "form": form,
    }

    return render(
        request,
        "logs/edit_entry.html",
        context,
    )


@login_required
def delete_entry(request, entry_id):

    entry = get_object_or_404(
        Entry,
        id=entry_id,
    )

    if entry.log.owner != request.user:
        return redirect("logs")

    log = entry.log

    if request.method == "POST":
        entry.delete()
        return redirect(
            "log",
            log_id=log.id,
        )

    context = {
        "entry": entry,
        "log": log,
    }

    return render(
        request,
        "logs/delete_entry.html",
        context,
    )



@login_required
def edit_log(request, log_id):

    log = get_object_or_404(
        Log,
        id=log_id,
        owner=request.user,
    )

    if request.method != "POST":
        form = LogForm(instance=log)

    else:
        form = LogForm(
            request.POST,
            instance=log,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "log",
                log_id=log.id,
            )

    context = {
        "log": log,
        "form": form,
    }

    return render(
        request,
        "logs/edit_log.html",
        context,
    )

@login_required
def dashboard(request):
    today = timezone.now().date()
    start = today - timedelta(days=29)

    activity = (
        Entry.objects.filter(
            log__owner=request.user,
            created_at__date__gte=start
        )
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )
    activity_dict = {
        item["day"]: item["total"]
        for item in activity
    }


    labels = []

    values = []

    for i in range(30):

        day = start + timedelta(days=i)

        labels.append(day.strftime("%b %d"))

        values.append(
            activity_dict.get(day, 0)
        )



    logs = Log.objects.filter(owner=request.user)

    entries = Entry.objects.filter(
        log__owner=request.user
    )

    latest_log = logs.first()

    latest_entry = (
        entries
        .order_by("-created_at")
        .first()
    )

    recent_logs = logs[:5]

    context = {

        "logs_count": logs.count(),

        "entries_count": entries.count(),

        "latest_log": latest_log,

        "latest_entry": latest_entry,

        "recent_logs": recent_logs,

        "chart_labels": json.dumps(labels),

        "chart_values": json.dumps(values),

    }

    return render(
        request,
        "logs/dashboard.html",
        context,
    )