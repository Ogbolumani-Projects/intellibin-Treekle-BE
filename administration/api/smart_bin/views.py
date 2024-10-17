from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from authservice.models import CustomUser
from dashboard.models import BinCompartment, WasteBin
from dashboard.serializers import WasteBinSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    request=WasteBinSerializer,
    responses=None
)
@api_view(['GET',])
@authentication_classes((JWTTokenUserAuthentication,))
@permission_classes((IsAuthenticated,))
def smart_bin_detail(request, id):
    try:
        smart_bin = WasteBin.objects.get(id=id)
    except WasteBin.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = WasteBinSerializer(smart_bin)
    return Response(serializer.data)


@extend_schema(
    request=WasteBinSerializer,
    responses=None
)
@api_view(['PUT',])
@authentication_classes((JWTTokenUserAuthentication,))
@permission_classes((IsAuthenticated,))
def activate_smart_bin(request, id):
    try:
        smart_bin = WasteBin.objects.get(id=id)
    except WasteBin.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    smart_bin.is_active = True
    smart_bin.save()

    serializer = WasteBinSerializer(smart_bin)
    return Response(serializer.data)


@extend_schema(
    request=WasteBinSerializer,
    responses=None
)
@api_view(['PUT',])
@authentication_classes((JWTTokenUserAuthentication,))
@permission_classes((IsAuthenticated,))
def deactivate_smart_bin(request, id):
    try:
        smart_bin = WasteBin.objects.get(id=id)
    except WasteBin.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    smart_bin.is_active = False
    smart_bin.save()

    serializer = WasteBinSerializer(smart_bin)
    return Response(serializer.data)


@extend_schema(
    request=WasteBinSerializer,
    responses=None
)
@api_view(['POST',])
@authentication_classes((JWTTokenUserAuthentication,))
@permission_classes((IsAuthenticated,))
def create_smart_bin(request):
    try:
        try:
            request_data = request.data
            user_id = int(request_data['user'])
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        smart_bin = WasteBin.objects.create(user=user)
        print(request_data)
        serializer = WasteBinSerializer(smart_bin, request_data)

        if serializer.is_valid():
            BinCompartment.objects.create(
                parent_bin=smart_bin, type_of_waste="RECYCLABLE"
            )

            BinCompartment.objects.create(
                parent_bin=smart_bin, type_of_waste="NON_RECYCLABLE"
            )
            
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if serializer.errors:
            print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        print("Exception Error")
        raise e
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AllWasteBinsView(ListAPIView):
    queryset = WasteBin.objects.all()
    serializer_class = WasteBinSerializer
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('bin_level', 'battery_level',)
