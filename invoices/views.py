from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer
from .message import get_message
from custom_permissions.permission import *
from rest_framework.pagination import PageNumberPagination

# New
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 50
# New version
class InvoiceListCreateView(generics.ListCreateAPIView):

    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [IsAdminOrAccountant]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'client_name']
    search_fields = ['client_name']
    ordering_fields = ['amount', 'due_date', 'created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Invoice.objects.none()
        if user.role in ['admin', 'accountant']:
            return Invoice.objects.all()
        return Invoice.objects.filter(user=user)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "message": get_message("invoice_created", request.user),
                "invoice": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceSerializer
    # permission_classes = [IsAdminOrAccountant]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Invoice.objects.none()
        if user.role in ["admin", "accountant"]:
            return Invoice.objects.all()
        return Invoice.objects.filter(user=user)
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "message": get_message("invoice_updated", request.user),
                "invoice": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {"message": get_message("invoice_deleted", request.user)},
            status=status.HTTP_200_OK,
        )
# New
class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsOwnerOrAdmin]