from django.db import models
from django.contrib.auth.models import User

class BudgetPeriod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    spending_limit = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget_period = models.ForeignKey(BudgetPeriod, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)

class Payday(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget_period = models.ForeignKey(BudgetPeriod, on_delete=models.CASCADE)
    payday_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
