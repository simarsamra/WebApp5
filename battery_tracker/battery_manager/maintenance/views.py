from django.shortcuts import render, redirect
from django.utils.timezone import now
from datetime import timedelta, date
from django.http import JsonResponse
from django.contrib import messages
from .models import BatteryReplacementRecord, Machine, Component, Building, Battery
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max, Q

def home(request):
    today = date.today()
    two_months_later = today + timedelta(days=60)
    upcoming_replacements = []
    overdue_replacements = []

    for battery in Battery.objects.select_related('component__machine__building').all():
        # Find the latest replacement record for this battery
        last_record = battery.replacement_records.order_by('-replacement_date').first()
        if last_record:
            last_date = last_record.replacement_date
        else:
            continue

        if battery.replacement_interval_type == 'months' and battery.replacement_interval_months:
            next_due = last_date + timedelta(days=30 * battery.replacement_interval_months)
            record_info = {
                'battery': battery,
                'component': battery.component,
                'machine': battery.component.machine,
                'building': battery.component.machine.building,
                'last_replacement': last_date,
                'next_due': next_due,
            }
            if next_due < today:
                overdue_replacements.append(record_info)
            elif today <= next_due <= two_months_later:
                upcoming_replacements.append(record_info)
        elif battery.replacement_interval_type == 'alarm':
            record_info = {
                'battery': battery,
                'component': battery.component,
                'machine': battery.component.machine,
                'building': battery.component.machine.building,
                'last_replacement': last_date,
                'next_due': None,
            }
            # Only show as overdue if last replacement is over a year ago
            if last_date < today - timedelta(days=365):
                overdue_replacements.append(record_info)

    # Sort by due date
    upcoming_replacements.sort(key=lambda x: x['next_due'] or date.max)
    overdue_replacements.sort(key=lambda x: x['next_due'] or date.max)

    return render(request, 'maintenance/home.html', {
        'upcoming_replacements': upcoming_replacements,
        'overdue_replacements': overdue_replacements,
    })

def history(request):
    buildings = Building.objects.all()
    machines = Machine.objects.all()
    components = Component.objects.all()
    qs = BatteryReplacementRecord.objects.all().order_by('-replacement_date')

    building_id = request.GET.get('building')
    machine_id = request.GET.get('machine')
    component_id = request.GET.get('component')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if building_id:
        qs = qs.filter(battery__component__machine__building_id=building_id)
        machines = machines.filter(building_id=building_id)
    if machine_id:
        qs = qs.filter(battery__component__machine_id=machine_id)
        components = components.filter(machine_id=machine_id)
    if component_id:
        qs = qs.filter(battery__component_id=component_id)
    if date_from:
        qs = qs.filter(replacement_date__gte=date_from)
    if date_to:
        qs = qs.filter(replacement_date__lte=date_to)

    return render(request, 'maintenance/history.html', {
        'replacement_history': qs,
        'buildings': buildings,
        'machines': machines,
        'components': components,
    })

@login_required(login_url='/accounts/login/')
def log_replacement(request):
    buildings = Building.objects.all()
    if request.method == "POST":
        battery_id = request.POST.get("battery")
        replacement_date = request.POST.get("replacement_date")
        if battery_id and replacement_date:
            BatteryReplacementRecord.objects.create(
                battery_id=battery_id,
                replacement_date=replacement_date
            )
            messages.success(request, "Replacement logged successfully!")
            return redirect('history')
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

def export_history_csv(request):
    qs = BatteryReplacementRecord.objects.all().order_by('-replacement_date')

    building_id = request.GET.get('building')
    machine_id = request.GET.get('machine')
    component_id = request.GET.get('component')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if building_id:
        qs = qs.filter(battery__component__machine__building_id=building_id)
    if machine_id:
        qs = qs.filter(battery__component__machine_id=machine_id)
    if component_id:
        qs = qs.filter(battery__component_id=component_id)
    if date_from:
        qs = qs.filter(replacement_date__gte=date_from)
    if date_to:
        qs = qs.filter(replacement_date__lte=date_to)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="replacement_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['Building', 'Machine', 'Component', 'Battery', 'Replacement Date'])

    for record in qs:
        writer.writerow([
            record.battery.component.machine.building.name,
            str(record.battery.component.machine),
            str(record.battery.component),
            str(record.battery),
            record.replacement_date
        ])

    return response

@login_required
def profile(request):
    return render(request, 'maintenance/profile.html')



