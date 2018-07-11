from rest_framework.viewsets import ModelViewSet
from .serializers import AppointmentSerializer, DetailedAppointmentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from appointment.models import Appointment


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def retrieve(self, request, pk=None):
        appointment = get_object_or_404(self.queryset, pk=pk)
        serializer = DetailedAppointmentSerializer(appointment)
        return Response(serializer.data)
