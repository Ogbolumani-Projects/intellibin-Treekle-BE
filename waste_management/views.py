from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WasteDataSerializer
from .tasks import send_bin_full_notification

class WasteDataAPIView(APIView):
    def get(self, request):
        serializer = WasteDataSerializer(data=request.data)
        if serializer.is_valid():
            waste_data = serializer.save()
            send_bin_full_notification.delay(waste_data.bin.bin_id) 
            # You can add logic here to send data to frontend elements or trigger notifications
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    