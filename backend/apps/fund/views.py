from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from apps.fund.models import FundLog
from utils.pagination import StandardResultsSetPagination


class FundLogSerializer(ModelSerializer):
    class Meta:
        model = FundLog
        fields = "__all__"


class FundLogView(ListAPIView):
    # permission_classes = [IsAuthenticated, ]
    serializer_class = FundLogSerializer
    pagination_class = StandardResultsSetPagination

    queryset = FundLog.objects.order_by("-start_time").all()

    def get(self, request, *args, **kwargs):
        keyword = request.query_params.get("keyword", "")
        if keyword:
            queryset = FundLog.objects.filter(name__contains=keyword).order_by('id')
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
