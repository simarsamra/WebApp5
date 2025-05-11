from django.urls import path
from . import views

urlpatterns = [
    # ...existing urls...
    path('export_report_pdf/', views.export_report_pdf, name='export_report_pdf'),
]