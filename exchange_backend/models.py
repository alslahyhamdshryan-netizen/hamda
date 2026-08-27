from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ADMIN = "admin"
    CASHIER = "cashier"
    ROLES = [(ADMIN, "مدير"), (CASHIER, "موظف صرافة")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLES, default=CASHIER)
    branch_name = models.CharField(max_length=120, default="فرع السوق المركزي")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} — {self.get_role_display()}"

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name_ar = models.CharField(max_length=80)
    buy_rate = models.DecimalField(max_digits=12, decimal_places=4)
    sell_rate = models.DecimalField(max_digits=12, decimal_places=4)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} — {self.name_ar}"

class Customer(models.Model):
    name = models.CharField(max_length=160)
    phone = models.CharField(max_length=30, blank=True)
    identity_number = models.CharField(max_length=60, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    BUY = "buy"
    SELL = "sell"
    TYPES = [(BUY, "شراء"), (SELL, "بيع")]
    PENDING = "pending"
    COMPLETED = "completed"
    REVIEW = "review"
    STATUSES = [(PENDING, "قيد التنفيذ"), (COMPLETED, "مكتملة"), (REVIEW, "مراجعة")]
    reference = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="transactions")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=4, choices=TYPES)
    foreign_amount = models.DecimalField(max_digits=14, decimal_places=2)
    local_amount = models.DecimalField(max_digits=14, decimal_places=2)
    rate = models.DecimalField(max_digits=12, decimal_places=4)
    status = models.CharField(max_length=12, choices=STATUSES, default=COMPLETED)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_transactions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
