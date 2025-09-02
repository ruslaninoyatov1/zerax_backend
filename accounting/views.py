from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, F
from .models import Account, JournalEntry
from .serializers import AccountSerializer, JournalEntrySerializer
from .message import get_message
from costum_permissions.permission import *

# ---- Account Views ----
class AccountListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAdminOrAccountant]

    def get_queryset(self):
        return Account.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": get_message("account_created", request.user), "account": serializer.data},
            status=status.HTTP_201_CREATED,
        )

# ---- Journal Entry Views ----
class JournalEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAdminOrAccountant]

    def get_queryset(self):
        return JournalEntry.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": get_message("journal_created", request.user), "journal_entry": serializer.data},
            status=status.HTTP_201_CREATED,
        )

# ---- Balance Sheet View ----
class BalanceSheetView(APIView):
    permission_classes = [IsAdminOrAccountant]

    def get(self, request):
        # Group balances by account type
        accounts = Account.objects.all()
        result = {}

        for account in accounts:
            balance = (
                JournalEntry.objects.filter(account=account)
                .aggregate(total=Sum(F("debit") - F("credit")))["total"] or 0
            )
            result.setdefault(account.type, 0)
            result[account.type] += balance

        return Response(
            {
                "message": get_message("balance_sheet", request.user),
                "balance_sheet": result,
            },
            status=status.HTTP_200_OK,
        )
