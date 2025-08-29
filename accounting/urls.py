from django.urls import path
from . import views

urlpatterns = [
    # Accounts
    path("accounts/", views.AccountListCreateView.as_view(), name="account-list-create"),   # GET + POST

    # Journal Entries
    path("journals/", views.JournalEntryListCreateView.as_view(), name="journal-list-create"),  # GET + POST

    # Balance Sheet
    path("balance-sheet/", views.BalanceSheetView.as_view(), name="balance-sheet"),  # GET only
]
