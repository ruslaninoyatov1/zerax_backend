from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer
from .message import get_message
from custom_permissions.permission import *

class InvoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer
    # permission_classes = [IsAdminOrAccountant | AuthenticatedReadOnly]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Invoice.objects.none()
        return Invoice.objects.filter(user=self.request.user)

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
        if not self.request.user.is_authenticated:
            return Invoice.objects.none()
        return Invoice.objects.filter(user=self.request.user)

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
