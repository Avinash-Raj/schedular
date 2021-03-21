from rest_framework import serializers
from schedules.models import Schedule
from schedules.validators import DateValidator, EmployeeValidator


class ScheduleSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')

    class Meta:
        model = Schedule
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'user_email', 'duration', 'slot_id', 'created_at']
        read_only_fields = ('id', 'slot_id', 'created_at', 'duration')
        validators = [EmployeeValidator(), DateValidator()]

    def create(self, validated_data):
        validated_data['user'] = self.employee
        return Schedule.objects.create(**validated_data)
