from django_filters import rest_framework as filters
from users.models import User
from django.contrib.auth.models import Group


class UserRoleFilter(filters.FilterSet):
    role = filters.CharFilter(field_name="groups", method='filter_by_role')

    def filter_by_role(self, queryset, name, value):
        # construct the full lookup expression.
        lookup = '__'.join([name, 'name'])
        return queryset.filter(**{lookup: value})

    class Meta:
        model = User
        fields = ['role']
