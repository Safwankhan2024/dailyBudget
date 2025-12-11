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

    # Handle different period types
    today = date.today()
    beginning_date = current_period.start_date

    # For monthly periods, adjust the beginning date to the start of the current month
    if current_period.period_type == 'monthly':
        beginning_date = date(today.year, today.month, 1)

    today = date.today()

    # Calculate days remaining until next payday
    next_payday = Payday.objects.filter(budget_period=current_period, payday_date__gte=today).order_by('payday_date').first()
    days_remaining = (next_payday.payday_date - today).days if next_payday else None

    # Calculate total spent so far (from beginning date)
    transactions_from_beginning = Transaction.objects.filter(budget_period=current_period, date__gte=beginning_date)
    total_spent = sum(transaction.amount for transaction in transactions_from_beginning)

    # Calculate remaining balance from today's spending limit
    remaining_balance = current_period.total_balance - total_spent

    # Calculate day's limit before today's spending (previous day's remaining)
    if today > beginning_date:
        yesterday = today - timedelta(days=1)
        transactions_yesterday = Transaction.objects.filter(budget_period=current_period, date__lte=yesterday, date__gte=beginning_date)
        spent_yesterday = sum(t.amount for t in transactions_yesterday)
        days_limit_before_today = current_period.total_balance - spent_yesterday
    else:
        days_limit_before_today = current_period.total_balance

    # Get all transactions sorted by date (most recent first)
    all_transactions = Transaction.objects.filter(budget_period=current_period).order_by('-date')

    # Calculate cumulative balances for each transaction
    cumulative_balances = []
    running_balance = current_period.total_balance

    for transaction in all_transactions:
        if transaction.date >= beginning_date:
            running_balance -= transaction.amount
        cumulative_balances.append({
            'date': transaction.date,
            'amount': transaction.amount,
            'description': transaction.description,
            'new_balance': running_balance
        })

    # Calculate total spent till the beginning of the period
    total_spent_till_beginning = sum(t.amount for t in Transaction.objects.filter(budget_period=current_period, date__lt=beginning_date))

    return JsonResponse({
        'budget_period': {
            'start_date': current_period.start_date,
            'end_date': current_period.end_date,
            'total_balance': current_period.total_balance,
            'spending_limit': current_period.spending_limit,
            'period_type': current_period.period_type
        },
        'beginning_date': beginning_date,
        'transactions': cumulative_balances,
        'total_spent': total_spent,
        'remaining_balance': remaining_balance,
        'days_remaining': days_remaining,
        'days_limit_before_today': days_limit_before_today,
        'total_spent_till_beginning': total_spent_till_beginning
    })
