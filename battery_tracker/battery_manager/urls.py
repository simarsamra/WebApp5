from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    # ... your existing urls ...
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)