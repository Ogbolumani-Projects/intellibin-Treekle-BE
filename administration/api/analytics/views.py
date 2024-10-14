from datetime import datetime, timedelta, timezone
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from authservice.models import CustomUser
from dashboard.models import WastePickUp
from dashboard.serializers import WasteBinSerializer
from drf_spectacular.utils import extend_schema
from django.db.models import Q



@extend_schema(
    request=WasteBinSerializer,
    responses=None
)
@api_view(['GET',])
@authentication_classes((JWTTokenUserAuthentication,))
@permission_classes((IsAuthenticated,))
def user_analytics(request):
    user = CustomUser.objects.get(id=request.user.id)
    if not user.is_admin:
        return Response({"detail": "You are not authorized to view this page"}, status=status.HTTP_403_FORBIDDEN)
    
    total_signups = CustomUser.objects.count()
    true_activation = WastePickUp.objects.filter(status="Picked up").distinct("user").count()
    two_months_ago = datetime.now(timezone.utc) - timedelta(days=60)
    retention_count = WastePickUp.objects.filter(Q(status="Picked up") & Q(date_picked__gte=two_months_ago)).distinct("user").count()

    response: dict = {
        "total_signups": total_signups,
        "true_activation": true_activation,
        "retention_count": retention_count
    }
    return Response(response)