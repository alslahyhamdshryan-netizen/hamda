import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchange_backend.settings")
import django
django.setup()
from django.contrib.auth.models import User
from exchange_backend.models import Department, Employee, UserProfile

user, created = User.objects.get_or_create(username="admin")
user.set_password("Admin@12345")
user.first_name = "مدير النظام"
user.is_staff = True
user.is_superuser = True
user.save()
UserProfile.objects.update_or_create(user=user, defaults={"role": "admin", "branch_name": "المقر الرئيسي"})
for code, name in [("HR", "الموارد البشرية"), ("FIN", "المالية"), ("SAL", "المبيعات"), ("IT", "تقنية المعلومات")]:
    Department.objects.get_or_create(code=code, defaults={"name": name})
print("تم تجهيز النظام.")
print("اسم المستخدم: admin")
print("كلمة المرور: Admin@12345")
