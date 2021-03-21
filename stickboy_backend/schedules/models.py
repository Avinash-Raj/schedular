import uuid
from django.db import models
from users.models import User
from schedules.managers import ScheduleManager


class BaseModel(models.Model):
    """ Base model """
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = (
            'created_at',
            'updated_at',
        )


class Schedule(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    duration = models.PositiveIntegerField(default=30)
    slot_id = models.CharField(max_length=64, unique=True)

    objects = ScheduleManager()

    @property
    def get_slot_id(self):
        return '{user_id}_{start_time:0.0f}_{end_time:0.0f}'.format(
            user_id=self.user.id,
            start_time=self.start_time.timestamp(), 
            end_time=self.end_time.timestamp())

    def save(self, *args, **kwargs):
        # update slot_id on new instance
        if self._state.adding:
            self.slot_id = self.get_slot_id
        super().save(*args, **kwargs)
