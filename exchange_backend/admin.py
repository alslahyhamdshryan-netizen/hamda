from django.contrib import admin
from .models import Attendance, Department, Employee, LeaveRequest, Payroll, Task, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin): list_display = ("user", "role", "branch_name", "phone"); list_filter = ("role",)
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin): list_display = ("name", "code", "manager", "is_active"); list_filter = ("is_active",)
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin): list_display = ("employee_number", "full_name", "job_title", "department", "status", "hire_date"); list_filter = ("department", "status"); search_fields = ("full_name", "employee_number", "national_id")
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin): list_display = ("employee", "date", "check_in", "check_out", "status"); list_filter = ("date", "status", "employee__department")
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin): list_display = ("employee", "leave_type", "start_date", "end_date", "status", "approved_by"); list_filter = ("status", "leave_type"); search_fields = ("employee__full_name",)
@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin): list_display = ("employee", "month", "basic_salary", "allowances", "deductions", "net_salary", "paid"); list_filter = ("month", "paid")
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin): list_display = ("title", "assigned_to", "due_date", "status", "created_by"); list_filter = ("status",)
