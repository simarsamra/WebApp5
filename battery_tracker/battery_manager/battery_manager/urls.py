"""
URL configuration for battery_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from maintenance import views
from maintenance.views import export_history_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home page
    path('history/', views.history, name='history'),  # History page
    path('log-replacement/', views.log_replacement, name='log_replacement'),
    path('api/machines/', views.get_machines, name='api_machines'),
    path('api/components/', views.get_components, name='api_components'),
    path('api/batteries/', views.get_batteries, name='api_batteries'),
    path('history/export/', export_history_csv, name='export_history_csv'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.profile, name='profile'),
    path('export_report_pdf/', views.export_report_pdf, name='export_report_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
