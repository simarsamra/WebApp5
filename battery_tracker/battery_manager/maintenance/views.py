from django.shortcuts import render, redirect
from django.utils.timezone import now
from datetime import timedelta, date
from django.http import JsonResponse
from .models import BatteryReplacementRecord, Machine, Component

def home(request):
    print("Home view called")  # Debug print
    today = now().date()
    next_two_months = today + timedelta(days=60)

    # Fetch upcoming replacements
    upcoming_replacements = BatteryReplacementRecord.objects.filter(
        due_date__gte=today, due_date__lte=next_two_months
    ).order_by('due_date')
    print(f"Upcoming replacements: {upcoming_replacements}")  # Debug print

    # Fetch overdue replacements
    overdue_replacements = BatteryReplacementRecord.objects.filter(
        due_date__lt=today
    ).order_by('due_date')
    print(f"Overdue replacements: {overdue_replacements}")  # Debug print

    return render(request, 'maintenance/home.html', {
        'upcoming_replacements': upcoming_replacements,
        'overdue_replacements': overdue_replacements,
    })



