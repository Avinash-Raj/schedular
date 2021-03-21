from django.db import models
from django.db.models import Q
from django.db.models.functions import TruncDate
from django.contrib.auth.models import AbstractUser, UserManager


class ScheduleManager(models.Manager):
    def is_slot_available(self, employee, start_dt, end_dt):
        """
        Check for slot available for the employee on given timeframe.
        """
        start_date = start_dt.date()
        end_date = end_dt.date()
        start_timestamp = start_dt.timestamp()
        end_timestamp = end_dt.timestamp()

        qs = self.filter(
            Q(user=employee),
            Q(start_time__date=start_date) | Q(start_time__date=end_date) | Q(end_time__date=start_date) | Q(end_time__date=end_date)
        )

        for schedule in qs:
            _, db_start_timestamp, db_end_timestamp = schedule.slot_id.split('_')
            db_start_timestamp = int(db_start_timestamp)
            db_end_timestamp = int(db_end_timestamp)

            # check for entries exists on the give timeframe
            if (db_start_timestamp <= start_timestamp <= db_end_timestamp) or (db_start_timestamp <= end_timestamp <= db_end_timestamp):
                return False

        return True
