

from django.urls import path
from .views import get_budget_data

urlpatterns = [
    path('api/budget/', get_budget_data, name='budget-data'),
]

