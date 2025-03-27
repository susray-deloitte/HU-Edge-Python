from django.urls import path
from .views import (
    OccasionCreateView,
    ExpenditureCreateView,
    ClearExpenseView,
    OccasionExpenditureSummaryView,
)

urlpatterns = [
    path('occasions/', OccasionCreateView.as_view(), name='occasion-create'),
    path('expenditures/', ExpenditureCreateView.as_view(), name='expenditure-create'),
    path('clear-expense/', ClearExpenseView.as_view(), name='clear-expense'),
    path('occasions/<int:pk>/summary/', OccasionExpenditureSummaryView.as_view(), name='occasion-summary'),
]