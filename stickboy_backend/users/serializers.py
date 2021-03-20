from django.conf import settings
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token


User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

    default_error_messages = {
        'not_found': _('Group not found.'),
        'invalid_group': _('Invalid group.')
    }

    def to_internal_value(self, validated_data):
        group = Group.objects.filter(**validated_data).first()
        if not group:
            raise serializers.ValidationError(self.error_messages['not_found'])
        return group

    def validate_name(self, name):
        if not name in settings.USER_GROUPS:
            raise serializers.ValidationError(self.error_messages['invalid_group'])
        return name


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        read_only_fields = ('date_joined', 'id', 'groups')
        fields = ("first_name", "last_name", "email", "password", "confirm_password", 'groups')
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'password': {'write_only': True},
            'email': {'write_only': True},
            'confirm_password': {'write_only': True},
        }
    
    def create(self, validated_data):
        user = None
        with transaction.atomic():
            groups_data = validated_data.pop('groups')
            user = User.objects.create(**validated_data)
            for group_data in groups_data:
                user.groups.add(group_data)
        return user

    def validate(self, attrs):
        """
        Validate input form values
        """
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")

        del attrs['confirm_password']
        attrs['password'] = make_password(attrs['password'])
        return attrs


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(request=self.context.get('request'), email=attrs.get("email"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token", "created")


class UserListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(method_name='get_role')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role')
        read_only_fields = (
            'email', 'first_name', 'last_name'
        )

    def get_role(self, obj):
        groups = obj.groups.filter(name__in=['admin', 'employee'])
        if not groups:
            return ''
        return groups[0].name
