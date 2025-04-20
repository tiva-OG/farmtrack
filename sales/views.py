from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Sale
from .serializers import SaleSerializer


class SaleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Sale.objects.filter(user=user).order_by("-entry_date")
