from rest_framework import serializers
from rest_framework.utils.representation import smart_repr
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from schedules.models import Schedule
from users.models import User


class DateValidator:
    """
    Validator for checking if a start date is before an end date field, check slot available or not, etc.
    """
    requires_context = True
    error_messages = {
        'date_before': _('{start_date_field} should be before {end_date_field}.'),
        'past_date': '{field} date should be a future date',
        'exceeds_duration': 'Slot duration should be a maximum of {duration} mins',
        'slot_not_available': 'No free slot available between {start_time} {end_time} for {employee}',
        'invalid_time_range': 'Start and end time should falls between 9AM and 6PM',
        'invalid_day': 'Schedules should be created on working days only(ie. Monday to Friday)'
    }

    def __init__(self, start_date_field="start_time", end_date_field="end_time"):
        self.start_date_field = start_date_field
        self.end_date_field = end_date_field

    def __call__(self, attrs, serializer):
        # check for both start and endtime greater than the current time
        if attrs['start_time'] < timezone.now():
            message = self.error_messages['past_date'].format(field=self.start_date_field)
            raise serializers.ValidationError({self.start_date_field: message}, code='past_date')

        if attrs['end_time'] < timezone.now():
            message = self.error_messages['past_date'].format(field=self.end_date_field)
            raise serializers.ValidationError({self.end_date_field: message}, code='past_date')

        # check for slot start_dt greater than end_dt or not
        if attrs['start_time'] > attrs['end_time']:
            message = self.error_messages['date_before'].format(
                start_date_field=self.start_date_field,
                end_date_field=self.end_date_field,
            )

            raise serializers.ValidationError({self.start_date_field: message}, code='date_before')

        # check for slot duration exceeds the limit or not
        time_diff = (attrs['end_time'] - attrs['start_time'])
        mins = (time_diff.total_seconds()//60)
        if mins > settings.SCHEDULE_SLOT_DURATION_IN_MINUTES:
            message = self.error_messages['exceeds_duration'].format(
                duration=settings.SCHEDULE_SLOT_DURATION_IN_MINUTES,
            )

            raise serializers.ValidationError({self.start_date_field: message}, code='exceeds_duration')

        # check for the timeframe falls under 9AM to 6PM on working days
        if not(9 <= attrs['start_time'].time().hour <= 18 and 9 <= attrs['end_time'].time().hour <= 18):
            raise serializers.ValidationError({self.start_date_field: self.error_messages['invalid_time_range']}, code='invalid_time_range')

        if attrs['start_time'].weekday() in [5, 6] or attrs['end_time'].weekday() in [5, 6]:
            raise serializers.ValidationError({self.start_date_field: self.error_messages['invalid_day']}, code='invalid_day')

        # check for slot available or not
        user = serializer.employee
        if not Schedule.objects.is_slot_available(user, attrs['start_time'], attrs['end_time']):
            message = self.error_messages['slot_not_available'].format(
                start_time=attrs['start_time'],
                end_time=attrs['end_time'],
                employee=user
            )

            raise serializers.ValidationError({self.start_date_field: message}, code='slot_not_available')

    def __repr__(self):
        return '<%s(start_date_field=%s, end_date_field=%s)>' % (
            self.__class__.__name__,
            smart_repr(self.start_date_field),
            smart_repr(self.end_date_field)
        )


class EmployeeValidator:
    """
    Validator to check the target user is an employee or not
    """
    requires_context = True
    error_messages = {
        'not_employee': _('You can create slot only for employees.'),
        'not_found': _('User not found.')
    }

    def __init__(self, field_name='user'):
        self.field_name = field_name

    def __call__(self, attrs, serializer):
        try:
            user = User.objects.get(email=attrs['user']['email'])
            if not user.is_employee:
                raise serializers.ValidationError({self.field_name: self.error_messages['not_employee']}, code='not_employee')
            serializer.employee = user
        except User.DoesNotExist:
            raise serializers.ValidationError({self.field_name: self.error_messages['not_found']}, code='not_found')
