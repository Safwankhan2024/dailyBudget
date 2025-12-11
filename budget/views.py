from django.shortcuts import render
from django.http import JsonResponse
from .models import BudgetPeriod, Transaction, Payday
from datetime import date, timedelta

def get_budget_data(request):
    # Get current user's budget data
    user = request.user

    # Get current budget period (most recent)
    current_period = BudgetPeriod.objects.filter(user=user).order_by('-start_date').first()

    if not current_period:
        return JsonResponse({'error': 'No budget period found'})

    # Calculate days remaining until next payday
    today = date.today()
    next_payday = Payday.objects.filter(budget_period=current_period, payday_date__gte=today).order_by('payday_date').first()

    if not next_payday:
        return JsonResponse({'error': 'No upcoming payday found'})

    days_remaining = (next_payday.payday_date - today).days

    # Calculate total spent so far
    transactions_today = Transaction.objects.filter(budget_period=current_period, date__lte=today)
    total_spent = sum(transaction.amount for transaction in transactions_today)

    # Calculate remaining balance from today's spending limit
    remaining_balance = current_period.total_balance - total_spent

    # Get all transactions sorted by date (most recent first)
    all_transactions = Transaction.objects.filter(budget_period=current_period).order_by('-date')

    return JsonResponse({
        'budget_period': {
            'start_date': current_period.start_date,
            'end_date': current_period.end_date,
            'total_balance': current_period.total_balance,
            'spending_limit': current_period.spending_limit
        },
        'transactions': [{
            'date': transaction.date,
            'amount': transaction.amount,
            'description': transaction.description,
            'new_balance': remaining_balance - (current_period.total_balance - sum(t.amount for t in Transaction.objects.filter(budget_period=current_period, date__lte=transaction.date)))
        } for transaction in all_transactions],
        'total_spent': total_spent,
        'remaining_balance': remaining_balance,
        'days_remaining': days_remaining
    })
