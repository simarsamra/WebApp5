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
from django.contrib.auth import views as auth_views  # Import auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('log-replacement/', views.log_replacement, name='log_replacement'),
    path('api/machines/', views.get_machines, name='api_machines'),
    path('api/components/', views.get_components, name='api_components'),
    path('api/batteries/', views.get_batteries, name='api_batteries'),
    path('history/export/', export_history_csv, name='export_history_csv'),

    # Include most auth URLs, but override password change ones
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('accounts/password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change_form.html'  # Explicitly point to your custom template
         ),
         name='password_change'),
    path('accounts/password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'  # Explicitly point to your custom template
         ),
         name='password_change_done'),

    # You might need to add other auth URLs if you use them (password reset, etc.)
    # or use include('django.contrib.auth.urls') and hope the DIRS setting works.
    # For now, let's be explicit for password change.
    # path('accounts/', include('django.contrib.auth.urls')), # Comment this out if defining manually above

    path('accounts/profile/', views.profile, name='profile'),
    path('export_report_pdf/', views.export_report_pdf, name='export_report_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
