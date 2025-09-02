from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
from .message import get_message
from costum_permissions.permission import *

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "message": get_message("expense_created", request.user),
                "expense": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


