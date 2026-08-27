from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.frontend_view),
    path("api/auth/csrf/", views.csrf_view), path("api/auth/login/", views.login_view), path("api/auth/me/", views.me_view), path("api/auth/logout/", views.logout_view),
    path("api/dashboard/", views.dashboard_view), path("api/employees/", views.employee_create_view), path("api/leaves/<int:pk>/decision/", views.leave_decision_view),
    re_path(r"^assets/(?P<path>.*)$", views.frontend_asset),
    re_path(r"^(?P<path>.*)$", views.frontend_view),
]
