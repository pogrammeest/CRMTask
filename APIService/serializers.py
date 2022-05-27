from rest_framework import serializers
from django.contrib.auth.models import User
from APIService.models import RepairRequest, UserDetails, Staff


class LinkUserBaseSerializerMixin(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username")

    @staticmethod
    def get_username(obj):
        return obj.user.username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserDetailSerializer(LinkUserBaseSerializerMixin):
    repair_request = serializers.PrimaryKeyRelatedField(many=True, queryset=RepairRequest.objects.all())

    class Meta:
        model = UserDetails
        fields = '__all__'


class StaffSerializer(LinkUserBaseSerializerMixin):
    repair_tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=RepairRequest.objects.all())

    class Meta:
        model = Staff
        fields = '__all__'


class RepairRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairRequest
        fields = ['created', 'title', 'description', 'owner', 'responsible', 'status']
