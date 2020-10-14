from rest_framework.serializers import ModelSerializer
from apps.Fund.models import FundLog
from rest_framework.views import APIView


class LogSerializer(ModelSerializer):
    class Meta:
        model = FundLog
        fields = "__all__"


class LogView(APIView):
    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page') or 1
        page_size = request.query_params.get('page_size') or 10
