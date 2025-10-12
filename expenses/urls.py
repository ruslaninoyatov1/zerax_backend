from django.urls import path
from .views import ExpenseListCreateView, ExpenseDetailView

urlpatterns = [
    # List & Create
    path("", ExpenseListCreateView.as_view(), name="expense-list-create"),

    # Retrieve, Update, Delete
    path("expenses/<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail"),
]