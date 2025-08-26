from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from datetime import datetime


def expense_list(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    expenses = Expense.objects.all()

    if month and year:
        expenses = expenses.filter(date__year=year, date__month=month)
    else:
        now = datetime.now()
        expenses = expenses.filter(date__year=now.year, date__month=now.month)

    total = sum(e.amount for e in expenses)
    return render(request, 'expense_list.html', {
        'expenses': expenses,
        'total': total,
        'month': month,
        'year': year,
    })


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})
