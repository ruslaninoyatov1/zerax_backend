from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
from .message import get_message

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAdminOrAccountant]

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


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAdminOrAccountant]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "message": get_message("expense_updated", request.user),
                "expense": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {"message": get_message("expense_deleted", request.user)},
            status=status.HTTP_200_OK,
        )
