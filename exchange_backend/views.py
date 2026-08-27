import json
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from .models import Currency, Customer, Transaction, UserProfile


def user_payload(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return {"id": user.id, "username": user.username, "name": user.get_full_name() or user.username, "role": profile.role, "role_label": profile.get_role_display(), "branch": profile.branch_name}

def api_error(message, status=400):
    return JsonResponse({"error": message}, status=status)

def home_view(request):
    return HttpResponseRedirect("/admin/")

@ensure_csrf_cookie
def csrf_view(request):
    return JsonResponse({"ok": True})

@require_http_methods(["POST"])
def login_view(request):
    try: data = json.loads(request.body or "{}")
    except json.JSONDecodeError: return api_error("بيانات الدخول غير صالحة")
    user = authenticate(request, username=data.get("username", ""), password=data.get("password", ""))
    if not user: return api_error("اسم المستخدم أو كلمة المرور غير صحيحة", 401)
    login(request, user)
    return JsonResponse({"user": user_payload(user)})

@login_required
def me_view(request): return JsonResponse({"user": user_payload(request.user)})

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({"ok": True})

@login_required
def dashboard_view(request):
    qs = Transaction.objects.select_related("customer", "currency").all()[:20]
    total_sales = Transaction.objects.filter(transaction_type=Transaction.SELL, status=Transaction.COMPLETED).aggregate(v=Sum("local_amount"))["v"] or Decimal("0")
    total_purchases = Transaction.objects.filter(transaction_type=Transaction.BUY, status=Transaction.COMPLETED).aggregate(v=Sum("local_amount"))["v"] or Decimal("0")
    data = [{"id": t.reference, "customer": t.customer.name, "type": t.get_transaction_type_display(), "amount": f"{t.foreign_amount} {t.currency.code}", "local": f"{t.local_amount} ر.س", "time": t.created_at.isoformat(), "status": t.get_status_display(), "color": "green" if t.transaction_type == Transaction.BUY else "red"} for t in qs]
    return JsonResponse({"currencies": list(Currency.objects.filter(is_active=True).values("code", "name_ar", "buy_rate", "sell_rate")), "transactions": data, "stats": {"sales": str(total_sales), "purchases": str(total_purchases), "profit": str(total_sales - total_purchases)}})

@login_required
@require_http_methods(["POST"])
def transaction_create_view(request):
    if not request.user.is_staff and getattr(getattr(request.user, "profile", None), "role", "cashier") not in ("admin", "cashier"):
        return api_error("ليس لديك صلاحية إنشاء العمليات", 403)
    try: data = json.loads(request.body or "{}")
    except json.JSONDecodeError: return api_error("بيانات العملية غير صالحة")
    required = ["customer", "currency", "transaction_type", "foreign_amount"]
    if any(not data.get(k) for k in required): return api_error("يرجى إكمال بيانات العملية")
    currency = Currency.objects.get(code=data["currency"])
    customer, _ = Customer.objects.get_or_create(name=data["customer"], defaults={"phone": data.get("phone", "")})
    amount = Decimal(str(data["foreign_amount"]))
    rate = currency.buy_rate if data["transaction_type"] == Transaction.BUY else currency.sell_rate
    t = Transaction.objects.create(reference=f"TX-{Transaction.objects.count()+10483}", customer=customer, currency=currency, transaction_type=data["transaction_type"], foreign_amount=amount, rate=rate, local_amount=amount * rate, created_by=request.user)
    return JsonResponse({"reference": t.reference, "ok": True}, status=201)
