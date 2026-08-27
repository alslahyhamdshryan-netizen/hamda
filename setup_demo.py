import os
from datetime import date, time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchange_backend.settings")
import django
django.setup()
from django.contrib.auth.models import User
from exchange_backend.models import Department, Employee, UserProfile, Attendance, LeaveRequest, Payroll, PerformanceReview, Task
user, _ = User.objects.get_or_create(username="admin")
user.set_password("Admin@12345"); user.first_name="مدير النظام"; user.is_staff=True; user.is_superuser=True; user.save()
UserProfile.objects.update_or_create(user=user, defaults={"role":"admin", "branch_name":"المقر الرئيسي"})
deps=[]
for code,name in [("HR","الموارد البشرية"),("FIN","المالية"),("SAL","المبيعات"),("IT","تقنية المعلومات"),("OPS","العمليات")]:
    deps.append(Department.objects.get_or_create(code=code, defaults={"name":name})[0])
people=[("EMP-001","أحمد محمد العريقي","مدير تقنية المعلومات","IT",7500,"ahmad@abdulilah.local"),("EMP-002","سارة عبدالله","أخصائية موارد بشرية","HR",6800,"sara@abdulilah.local"),("EMP-003","خالد علي","محاسب أول","FIN",6200,"khaled@abdulilah.local"),("EMP-004","نورة حسن","مسؤولة مبيعات","SAL",5900,"noura@abdulilah.local"),("EMP-005","ياسر سالم","منسق عمليات","OPS",5200,"yasser@abdulilah.local")]
for number,name,title,code,salary,email in people:
    e,_=Employee.objects.update_or_create(employee_number=number,defaults={"full_name":name,"job_title":title,"department":Department.objects.get(code=code),"hire_date":date(2023,1,10),"salary":salary,"email":email,"phone":"0500000000","status":Employee.ACTIVE})
    Attendance.objects.update_or_create(employee=e,date=date.today(),defaults={"status":Attendance.PRESENT if number not in ("EMP-004",) else Attendance.LATE,"check_in":time(8,0),"check_out":time(16,0)})
    Payroll.objects.update_or_create(employee=e,month=date(date.today().year,date.today().month,1),defaults={"basic_salary":salary,"allowances":1200,"deductions":300,"net_salary":salary+900,"paid":number in ("EMP-001","EMP-002")})
    PerformanceReview.objects.get_or_create(employee=e,reviewer=user,review_date=date.today(),defaults={"score":4,"strengths":"التزام وتعاون جيد","goals":"رفع كفاءة الأداء خلال الربع القادم"})
    Task.objects.get_or_create(title=f"خطة تطوير {name}",assigned_to=e,created_by=user,defaults={"due_date":date.today(),"status":Task.PROGRESS,"description":"متابعة أهداف الموظف الشهرية"})
e=Employee.objects.get(employee_number="EMP-003")
LeaveRequest.objects.get_or_create(employee=e,leave_type="إجازة سنوية",start_date=date.today(),end_date=date.today(),defaults={"reason":"ظرف عائلي"})
print("تم تجهيز نظام عبد الإله HR والبيانات التجريبية.")
print("اسم المستخدم: admin")
print("كلمة المرور: Admin@12345")
