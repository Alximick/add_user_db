from django.contrib import admin
from debt.models import DebtType, Debt


class DebtType_Admin(admin.ModelAdmin):
    fields = ['name', 'slug']
    list_display = ['name', 'slug']
    search_fields = ['name']


class Debt_Admin(admin.ModelAdmin):
    fields = ['type', 'user', 'year', 'month', 'amount']
    list_display = ['type', 'user', 'amount']


admin.site.register(DebtType, DebtType_Admin)
admin.site.register(Debt, Debt_Admin)