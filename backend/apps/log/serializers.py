from rest_framework.serializers import ModelSerializer

from apps.log.models import Log


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = "__all__"
