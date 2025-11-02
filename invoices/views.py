# invoices/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Invoice
from .serializers import InvoiceSerializer
from .message import get_message
from custom_permissions.permission import IsOwnerOrAdmin


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class InvoiceListCreateView(generics.ListCreateAPIView):
    """
    - List: authenticated users see their invoices; admin/accountant see all.
    - Create: any authenticated user can create an invoice (it will be saved with request.user).
    """
    serializer_class = InvoiceSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]  # require auth to list/create
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'client_name']
    search_fields = ['client_name']
    ordering_fields = ['amount', 'due_date', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return Invoice.objects.none()

        if getattr(user, "role", None) in ("admin", "accountant"):
            return Invoice.objects.all()

        return Invoice.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
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
    """
    Detail/update/delete on a single invoice.
    - Uses object-level permission IsOwnerOrAdmin.
    - get_queryset restricts list of accessible objects (defensive).
    """
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return Invoice.objects.none()
        if getattr(user, "role", None) in ("admin", "accountant"):
            return Invoice.objects.all()
        return Invoice.objects.filter(user=user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
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
        # IsOwnerOrAdmin already denies if not allowed
        self.perform_destroy(instance)
        return Response({"message": get_message("invoice_deleted", request.user)}, status=status.HTTP_200_OK)
