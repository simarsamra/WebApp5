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
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.conf import settings
import os
import io
from PyPDF2 import PdfMerger, PdfReader

def get_upcoming_and_overdue_replacements():
    today = date.today()
    two_months_later = today + timedelta(days=60)
    upcoming_replacements = []
    overdue_replacements = []

    for battery in Battery.objects.select_related('component__machine__building').all():
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
            if last_date < today - timedelta(days=365):
                overdue_replacements.append(record_info)

    # Sort by due date
    upcoming_replacements.sort(key=lambda x: x['next_due'] or date.max)
    overdue_replacements.sort(key=lambda x: x['next_due'] or date.max)
    return upcoming_replacements, overdue_replacements

def home(request):
    upcoming_replacements, overdue_replacements = get_upcoming_and_overdue_replacements()

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

import io
from PyPDF2 import PdfMerger, PdfReader
from django.http import HttpResponse
import os
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_report_pdf(request):
    upcoming, overdue = get_upcoming_and_overdue_replacements()

    # 1. Collect unique procedures (PDFs only)
    procedures = {}
    for record in upcoming + overdue:
        doc = getattr(record['component'], 'procedure_document', None)
        if doc and doc.name.lower().endswith('.pdf') and doc.name not in procedures:
            procedures[doc.name] = doc

    # 2. Generate the main report in a buffer
    buffer_main = io.BytesIO()
    p = canvas.Canvas(buffer_main, pagesize=letter)
    width, height = letter
    y = height - 40

    def draw_report_section(records, section_title):
        nonlocal y
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, section_title)
        y -= 20
        p.setFont("Helvetica", 11)
        if not records:
            p.drawString(60, y, f"No {section_title.lower()}.")
            y -= 20
        else:
            for record in records:
                if y < 100:
                    p.showPage()
                    y = height - 40
                p.drawString(60, y, f"Component: {record['component']}")
                y -= 15
                p.drawString(80, y, f"Battery: {record['battery']}")
                y -= 15
                p.drawString(80, y, f"Machine: {record['machine']} | Building: {record['building']}")
                y -= 15
                p.drawString(80, y, f"Last replaced: {record['last_replacement']}")
                y -= 15
                if record['next_due']:
                    p.drawString(80, y, f"Due on: {record['next_due']}" if section_title == "Upcoming Replacements" else f"Overdue since: {record['next_due']}")
                    y -= 15
                else:
                    p.drawString(80, y, "Next due: On Alarm" if section_title == "Upcoming Replacements" else "Overdue (On Alarm)")
                    y -= 15
                doc = getattr(record['component'], 'procedure_document', None)
                if doc and doc.name.lower().endswith('.pdf'):
                    # Placeholder for page number, will fill in after merging
                    p.drawString(80, y, f"See Procedure: {doc.name} (see page ?)")
                    y -= 15
                y -= 10

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Battery Replacement Report")
    y -= 30
    draw_report_section(upcoming, "Upcoming Replacements")
    draw_report_section(overdue, "Overdue Replacements")
    p.save()
    buffer_main.seek(0)

    # 3. Count pages in main report and each procedure
    main_report_reader = PdfReader(buffer_main)
    main_report_pages = len(main_report_reader.pages)

    procedure_page_counts = {}
    for docname, doc in procedures.items():
        full_path = doc.path if os.path.isabs(doc.path) else os.path.join(settings.MEDIA_ROOT, doc.name)
        with open(full_path, 'rb') as f:
            reader = PdfReader(f)
            procedure_page_counts[docname] = len(reader.pages)

    # 4. Calculate starting page for each procedure
    procedure_start_pages = {}
    current_page = main_report_pages + 1  # PDF pages are 1-based
    for docname in procedures:
        procedure_start_pages[docname] = current_page
        current_page += procedure_page_counts[docname]

    # 5. Regenerate main report with page numbers for procedures
    buffer_final = io.BytesIO()
    p2 = canvas.Canvas(buffer_final, pagesize=letter)
    width, height = letter
    y = height - 40

    def draw_report_section_with_pages(records, section_title):
        nonlocal y
        p2.setFont("Helvetica-Bold", 14)
        p2.drawString(50, y, section_title)
        y -= 20
        p2.setFont("Helvetica", 11)
        if not records:
            p2.drawString(60, y, f"No {section_title.lower()}.")
            y -= 20
        else:
            for record in records:
                if y < 100:
                    p2.showPage()
                    y = height - 40
                p2.drawString(60, y, f"Component: {record['component']}")
                y -= 15
                p2.drawString(80, y, f"Battery: {record['battery']}")
                y -= 15
                p2.drawString(80, y, f"Machine: {record['machine']} | Building: {record['building']}")
                y -= 15
                p2.drawString(80, y, f"Last replaced: {record['last_replacement']}")
                y -= 15
                if record['next_due']:
                    p2.drawString(80, y, f"Due on: {record['next_due']}" if section_title == "Upcoming Replacements" else f"Overdue since: {record['next_due']}")
                    y -= 15
                else:
                    p2.drawString(80, y, "Next due: On Alarm" if section_title == "Upcoming Replacements" else "Overdue (On Alarm)")
                    y -= 15
                doc = getattr(record['component'], 'procedure_document', None)
                if doc and doc.name.lower().endswith('.pdf'):
                    page_num = procedure_start_pages.get(doc.name, '?')
                    p2.drawString(80, y, f"See Procedure: {doc.name} (see page {page_num})")
                    y -= 15
                y -= 10

    p2.setFont("Helvetica-Bold", 16)
    p2.drawString(50, y, "Battery Replacement Report")
    y -= 30
    draw_report_section_with_pages(upcoming, "Upcoming Replacements")
    draw_report_section_with_pages(overdue, "Overdue Replacements")
    p2.save()
    buffer_final.seek(0)

    # 6. Merge: main report (with page numbers), then each procedure PDF with bookmarks
    merger = PdfMerger()
    merger.append(buffer_final)
    for docname, doc in procedures.items():
        full_path = doc.path if os.path.isabs(doc.path) else os.path.join(settings.MEDIA_ROOT, doc.name)
        with open(full_path, 'rb') as f:
            merger.append(f, outline_item=f"Procedure: {docname}")

    output_buffer = io.BytesIO()
    merger.write(output_buffer)
    merger.close()
    output_buffer.seek(0)

    response = HttpResponse(output_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="battery_report.pdf"'
    return response



