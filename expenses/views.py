from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status,filters
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
from .message import get_message
from custom_permissions.permission import *
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsUser | IsAdminOrAccountant]

    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['category','date']
    search_fields = ['note']
    ordering_fields = ['amount','date','created_at']

    def get_queryset(self):
        user = self.request.user
        queryset = Expense.objects.filter(user=user)

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date_range=[start_date,end_date])
        return queryset


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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_amount = queryset.aggregate(Sum("amount"))["amount__sum"] or 0
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response({
            "total_expense": total_amount,
            "results": serializer.data
        })

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsUser | IsAdminOrAccountant]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin','accountant']:
            return Expense.objects.all()
        return Expense.objects.filter(user=user)

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