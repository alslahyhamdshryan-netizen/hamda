import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from .models import Attendance, Department, Employee, LeaveRequest, Payroll, Task, UserProfile

def user_payload(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return {"id": user.id, "username": user.username, "name": user.get_full_name() or user.username, "role": profile.role, "role_label": profile.get_role_display(), "branch": profile.branch_name}
def api_error(message, status=400): return JsonResponse({"error": message}, status=status)
def home_view(request): return HttpResponseRedirect("/admin/")
@ensure_csrf_cookie
def csrf_view(request): return JsonResponse({"ok": True})
@require_http_methods(["POST"])
def login_view(request):
    try: data = json.loads(request.body or "{}")
    except json.JSONDecodeError: return api_error("بيانات الدخول غير صالحة")
    user = authenticate(request, username=data.get("username", ""), password=data.get("password", ""))
    if not user: return api_error("اسم المستخدم أو كلمة المرور غير صحيحة", 401)
    login(request, user); return JsonResponse({"user": user_payload(user)})
@login_required
def me_view(request): return JsonResponse({"user": user_payload(request.user)})
@require_http_methods(["POST"])
def logout_view(request): logout(request); return JsonResponse({"ok": True})

def can_manage(user): return user.is_staff or getattr(getattr(user, "profile", None), "role", "employee") in ("admin", "hr")
@login_required
def dashboard_view(request):
    today = timezone.localdate()
    employees = Employee.objects.select_related("department").all()
    pending_leaves = LeaveRequest.objects.filter(status=LeaveRequest.PENDING).count()
    active = employees.filter(status=Employee.ACTIVE).count()
    present = Attendance.objects.filter(date=today, status=Attendance.PRESENT).count()
    recent = employees.order_by("-created_at")[:8]
    return JsonResponse({"stats": {"employees": employees.count(), "active": active, "present": present, "pending_leaves": pending_leaves}, "departments": list(Department.objects.annotate(total=Count("employees")).values("name", "code", "total")), "employees": [{"id": e.id, "number": e.employee_number, "name": e.full_name, "title": e.job_title, "department": e.department.name, "status": e.get_status_display(), "email": e.email, "phone": e.phone, "hire_date": e.hire_date.isoformat()} for e in recent], "leave_requests": list(LeaveRequest.objects.select_related("employee").filter(status=LeaveRequest.PENDING).values("id", "employee__full_name", "leave_type", "start_date", "end_date", "status")[:6] ), "payroll_total": str(Payroll.objects.filter(month__month=today.month, month__year=today.year).aggregate(v=Sum("net_salary"))["v"] or 0)})
@login_required
@require_http_methods(["POST"])
def employee_create_view(request):
    if not can_manage(request.user): return api_error("هذه العملية متاحة للمدير أو مسؤول الموارد البشرية فقط", 403)
    try: data = json.loads(request.body or "{}")
    except json.JSONDecodeError: return api_error("بيانات الموظف غير صالحة")
    required = ["employee_number", "full_name", "job_title", "department", "hire_date"]
    if any(not data.get(k) for k in required): return api_error("يرجى إكمال بيانات الموظف")
    department = Department.objects.get(id=data["department"])
    employee = Employee.objects.create(employee_number=data["employee_number"], full_name=data["full_name"], job_title=data["job_title"], department=department, hire_date=data["hire_date"], email=data.get("email", ""), phone=data.get("phone", ""), national_id=data.get("national_id", ""), salary=data.get("salary", 0))
    return JsonResponse({"ok": True, "id": employee.id}, status=201)
@login_required
@require_http_methods(["POST"])
def leave_decision_view(request, pk):
    if not can_manage(request.user): return api_error("ليست لديك صلاحية اعتماد الإجازات", 403)
    try: data = json.loads(request.body or "{}")
    except json.JSONDecodeError: return api_error("بيانات القرار غير صالحة")
    leave = LeaveRequest.objects.get(pk=pk); decision = data.get("status")
    if decision not in (LeaveRequest.APPROVED, LeaveRequest.REJECTED): return api_error("القرار غير صالح")
    leave.status = decision; leave.approved_by = request.user; leave.save(update_fields=["status", "approved_by"])
    return JsonResponse({"ok": True})
