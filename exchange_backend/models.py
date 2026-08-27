from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ADMIN = "admin"
    HR = "hr"
    EMPLOYEE = "employee"
    ROLES = [(ADMIN, "مدير النظام"), (HR, "مسؤول الموارد البشرية"), (EMPLOYEE, "موظف")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLES, default=EMPLOYEE)
    branch_name = models.CharField(max_length=120, default="المقر الرئيسي")
    phone = models.CharField(max_length=30, blank=True)

class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=20, unique=True)
    manager = models.ForeignKey("Employee", null=True, blank=True, on_delete=models.SET_NULL, related_name="managed_departments")
    is_active = models.BooleanField(default=True)

    def __str__(self): return self.name

class Employee(models.Model):
    ACTIVE = "active"
    ON_LEAVE = "leave"
    INACTIVE = "inactive"
    STATUSES = [(ACTIVE, "على رأس العمل"), (ON_LEAVE, "في إجازة"), (INACTIVE, "غير نشط")]
    employee_number = models.CharField(max_length=30, unique=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="employee")
    full_name = models.CharField(max_length=160)
    national_id = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    job_title = models.CharField(max_length=120)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="employees")
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUSES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.employee_number} — {self.full_name}"

class Attendance(models.Model):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    STATUSES = [(PRESENT, "حاضر"), (ABSENT, "غائب"), (LATE, "متأخر")]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=PRESENT)
    notes = models.TextField(blank=True)
    class Meta: unique_together = ("employee", "date")

class LeaveRequest(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    STATUSES = [(PENDING, "قيد المراجعة"), (APPROVED, "مقبولة"), (REJECTED, "مرفوضة")]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=60, default="إجازة سنوية")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=PENDING)
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payroll")
    month = models.DateField(help_text="أول يوم من شهر الاستحقاق")
    basic_salary = models.DecimalField(max_digits=14, decimal_places=2)
    allowances = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=14, decimal_places=2)
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    class Meta: unique_together = ("employee", "month")

class Task(models.Model):
    TODO = "todo"
    PROGRESS = "progress"
    DONE = "done"
    STATUSES = [(TODO, "جديدة"), (PROGRESS, "قيد التنفيذ"), (DONE, "مكتملة")]
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name="tasks")
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=TODO)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
