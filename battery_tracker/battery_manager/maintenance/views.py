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

def log_replacement(request):
    # Load initial data for the dropdowns
    buildings = Machine.objects.values_list('building', flat=True).distinct()
    initial_records = BatteryReplacementRecord.objects.all()
    
    context = {
        'buildings': buildings,
        'records': initial_records,
        'today': date.today(),
    }
    return render(request, 'maintenance/log_replacement.html', context)

def get_machines(request):
    building = request.GET.get('building')
    machines = Machine.objects.all()
    if building:
        machines = machines.filter(building=building)
    
    data = [{
        'id': machine.id,
        'model': machine.model,
        'machine_id': machine.machine_id
    } for machine in machines]
    return JsonResponse(data, safe=False)

def get_records(request):
    building = request.GET.get('building')
    machine_id = request.GET.get('machine')
    
    records = BatteryReplacementRecord.objects.all()
    if building:
        records = records.filter(component__machine__building=building)
    if machine_id:
        records = records.filter(component__machine_id=machine_id)
    
    data = [{
        'id': record.id,
        'component': {
            'machine': {
                'building': record.component.machine.building,
                'model': record.component.machine.model
            },
            'component_model': str(record.component.component_model)
        },
        'due_date': record.due_date.strftime('%Y-%m-%d')
    } for record in records]
    return JsonResponse(data, safe=False)

def history(request):
    records = BatteryReplacementRecord.objects.all().order_by('-last_replaced')
    return render(request, 'maintenance/history.html', {'records': records})
