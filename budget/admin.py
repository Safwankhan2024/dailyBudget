from django.contrib import admin
from .models import BudgetPeriod, Transaction, Payday

admin.site.register(BudgetPeriod)
admin.site.register(Transaction)
admin.site.register(Payday)
