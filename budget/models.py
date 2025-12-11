from django.db import models
from django.contrib.auth.models import User

class BudgetPeriod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(db_index=True)  # Add index for date queries
    end_date = models.DateField()
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    spending_limit = models.DecimalField(max_digits=10, decimal_places=2)

    # Budget period type: 'monthly', 'custom', or 'pay_period'
    period_type = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'),
        ('custom', 'Custom Dates'),
        ('pay_period', 'Pay Period')
    ], default='monthly')

    class Meta:
        indexes = [
            models.Index(fields=['user', 'start_date']),  # Optimize for user period queries
        ]

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget_period = models.ForeignKey(BudgetPeriod, on_delete=models.CASCADE)
    date = models.DateField(db_index=True)  # Add index for date-based filtering
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['budget_period', 'date']),  # Optimize for period/date queries
            models.Index(fields=['user', 'date']),  # Optimize for user date range queries
        ]

class Payday(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget_period = models.ForeignKey(BudgetPeriod, on_delete=models.CASCADE)
    payday_date = models.DateField(db_index=True)  # Add index for date queries
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['budget_period', 'payday_date']),  # Optimize for period payday queries
        ]
