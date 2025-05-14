from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('export_report_pdf/', views.export_report_pdf, name='export_report_pdf'),
    #path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    #path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    # ...add your app-specific views here...
]