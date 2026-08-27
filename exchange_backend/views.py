import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import FileResponse, JsonResponse, HttpResponseRedirect
from pathlib import Path
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from .models import Attendance, Department, Employee, LeaveRequest, Payroll, Task, UserProfile

def user_payload(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return {"id": user.id, "username": user.username, "name": user.get_full_name() or user.username, "role": profile.role, "role_label": profile.get_role_display(), "branch": profile.branch_name}
def api_error(message, status=400): return JsonResponse({"error": message}, status=status)
def home_view(request): return HttpResponseRedirect("/admin/")

def frontend_view(request, path=""):
    index = Path(settings.BASE_DIR) / "dist" / "public" / "index.html"
    if index.exists():
        return FileResponse(index.open("rb"), content_type="text/html")
    return HttpResponseRedirect("/admin/")

def frontend_asset(request, path):
    from django.views.static import serve
    return serve(request, path, document_root=str(Path(settings.BASE_DIR) / "dist" / "public" / "assets"))
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

@login_required
def report_daily_view(request):
    if not can_manage(request.user): return api_error("التقارير متاحة للإدارة فقط", 403)
    date_text = request.GET.get("date") or str(timezone.localdate())
    from datetime import date
    try: report_date = date.fromisoformat(date_text)
    except ValueError: return api_error("التاريخ غير صحيح")
    attendance = Attendance.objects.filter(date=report_date)
    payroll = Payroll.objects.filter(month__year=report_date.year, month__month=report_date.month)
    return JsonResponse({"date": str(report_date), "employees": Employee.objects.count(), "attendance": {"present": attendance.filter(status="present").count(), "absent": attendance.filter(status="absent").count(), "late": attendance.filter(status="late").count()}, "leave_requests": LeaveRequest.objects.filter(created_at__date=report_date).count(), "payroll_total": str(payroll.aggregate(v=Sum("net_salary"))["v"] or 0), "tasks_done": Task.objects.filter(status=Task.DONE, created_at__date=report_date).count()})

@login_required
@require_http_methods(["POST"])
def attendance_create_view(request):
    try: data = json.loads(request.body or "{}")
    except json.JSONDecodeError: return api_error("بيانات الحضور غير صالحة")
    if not data.get("employee_id"): return api_error("الموظف مطلوب")
    record, _ = Attendance.objects.update_or_create(employee_id=data["employee_id"], date=data.get("date", timezone.localdate()), defaults={"status": data.get("status", "present"), "check_in": data.get("check_in"), "check_out": data.get("check_out"), "notes": data.get("notes", "")})
    return JsonResponse({"ok": True, "id": record.id}, status=201)

@login_required
@require_http_methods(["POST"])
def leave_create_view(request):
    try: data = json.loads(request.body or "{}")
    except json.JSONDecodeError: return api_error("بيانات الإجازة غير صالحة")
    leave = LeaveRequest.objects.create(employee_id=data.get("employee_id"), leave_type=data.get("leave_type", "إجازة سنوية"), start_date=data["start_date"], end_date=data["end_date"], reason=data.get("reason", ""))
    return JsonResponse({"ok": True, "id": leave.id}, status=201)
