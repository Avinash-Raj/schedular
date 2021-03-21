from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from schedules.serializers import ScheduleSerializer
from schedules.models import Schedule
from users.permission import IsAdminUser


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    Views related to employee schedule.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()
