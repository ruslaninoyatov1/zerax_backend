from django.urls import path
from .views import ExpenseListCreateView    

urlpatterns = [
    path("", ExpenseListCreateView.as_view(), name="expense-list-create"),
]
