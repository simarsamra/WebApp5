from django.shortcuts import render, redirect
from django.utils.timezone import now
from datetime import timedelta, date
from django.http import JsonResponse
from .models import BatteryReplacementRecord, Machine, Component, Building, Battery

def home(request):
    today = date.today()
    upcoming_replacements = BatteryReplacementRecord.objects.filter(
        replacement_date__gte=today
    ).order_by('replacement_date')
    overdue_replacements = BatteryReplacementRecord.objects.filter(
        replacement_date__lt=today
    ).order_by('replacement_date')

    return render(request, 'maintenance/home.html', {
        'upcoming_replacements': upcoming_replacements,
        'overdue_replacements': overdue_replacements,
    })

def history(request):
    replacement_history = BatteryReplacementRecord.objects.all().order_by('-replacement_date')

    return render(request, 'maintenance/history.html', {
        'replacement_history': replacement_history,
    })

def log_replacement(request):
    buildings = Building.objects.all()
    return render(request, 'maintenance/log_replacement.html', {
        'buildings': buildings,
        'today': date.today(),
    })

# API Endpoints for filtering
def get_machines(request):
    building_id = request.GET.get('building')
    machines = Machine.objects.filter(building_id=building_id) if building_id else Machine.objects.all()
    data = [
        {
            'id': m.id,
            'label': f"{m.model} ({m.machine_id})"
        }
        for m in machines
    ]
    return JsonResponse(data, safe=False)

def get_components(request):
    machine_id = request.GET.get('machine')
    components = Component.objects.filter(machine_id=machine_id) if machine_id else Component.objects.all()
    data = [
        {
            'id': c.id,
            'label': f"{c.name} ({c.model_number}) - {c.oem}"
        }
        for c in components
    ]
    return JsonResponse(data, safe=False)

def get_batteries(request):
    component_id = request.GET.get('component')
    batteries = Battery.objects.filter(component_id=component_id) if component_id else Battery.objects.all()
    data = [
        {
            'id': b.id,
            'label': f"{b.oem} ({b.oem_part_number})"
        }
        for b in batteries
    ]
    return JsonResponse(data, safe=False)



