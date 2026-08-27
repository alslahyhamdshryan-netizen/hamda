# صَرافة — أساس Django

تم تحويل الواجهة إلى لوحة تشغيل عربية لنظام صرافة، مع إضافة أساس Django قابل للربط بها.

## المكونات الحالية

- لوحة ملخص الصندوق والإيرادات والمشتريات وصافي الربح.
- شاشة أسعار العملات مع شراء/بيع وتغير السعر.
- سجل العمليات مع بحث وتصفية وتصدير كعناصر واجهة.
- نموذج عملية صرف جديد تفاعلي.
- هيكل Django يضم نماذج `Currency` و`Customer` و`Transaction` ولوحة إدارة Django.

## تشغيل Django محليًا

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

الواجهة الحالية تعمل عبر Vite كما كانت في المستودع، بينما يوفر Django طبقة البيانات والإدارة الخلفية عند ربط API في المرحلة التالية. بيانات اللوحة الحالية تجريبية لأغراض العرض، ولا ينبغي استخدامها في تشغيل مالي حقيقي قبل إضافة المصادقة، الصلاحيات، التدقيق المحاسبي، وقاعدة بيانات إنتاجية.

## الربط بالمصادقة والواجهة

أصبح خادم الواجهة يمرر `/api/*` إلى Django عبر المتغير `DJANGO_API_URL` (القيمة الافتراضية `http://127.0.0.1:8000`). شغّل الخدمتين في نافذتين:

```bash
python manage.py migrate
python manage.py runserver 8000
pnpm dev
```

ينفذ React طلب `api/auth/login/`، ويحفظ Django جلسة المستخدم، ثم يطلب `api/auth/me/` عند فتح الصفحة. يتم إرسال CSRF token مع طلبات POST. أنشئ المستخدمين من `/admin/`، ثم أضف `UserProfile` لكل مستخدم وحدد الدور `admin` أو `cashier`. المدير يستطيع إدارة البيانات من Django Admin، بينما موظف الصرافة يستطيع إنشاء عمليات الصرف من الواجهة وفق الصلاحية المطبقة في API.

في الإنتاج، عيّن `DJANGO_API_URL` إلى عنوان خدمة Django، واضبط `SECRET_KEY`، و`DEBUG=False`، و`ALLOWED_HOSTS`، واستخدم PostgreSQL أو MySQL بدل SQLite، مع HTTPS ونسخ احتياطية دورية.
