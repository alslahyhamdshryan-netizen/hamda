from django.contrib import admin
from .models import Currency, Customer, Transaction

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name_ar", "buy_rate", "sell_rate", "is_active")
    list_editable = ("buy_rate", "sell_rate", "is_active")

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ("name", "phone", "identity_number")
    list_display = ("name", "phone", "identity_number", "created_at")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("reference", "customer", "currency", "transaction_type", "foreign_amount", "local_amount", "status", "created_at")
    list_filter = ("transaction_type", "status", "currency")
    search_fields = ("reference", "customer__name")
    readonly_fields = ("created_at",)
