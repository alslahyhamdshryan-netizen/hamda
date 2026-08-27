from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view), path("admin/", admin.site.urls),
    path("api/auth/csrf/", views.csrf_view), path("api/auth/login/", views.login_view), path("api/auth/me/", views.me_view), path("api/auth/logout/", views.logout_view),
    path("api/dashboard/", views.dashboard_view), path("api/employees/", views.employee_create_view), path("api/leaves/<int:pk>/decision/", views.leave_decision_view),
]
