from rest_framework.serializers import ModelSerializer
from apps.Fund.models import FundLog
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


class FundLogSerializer(ModelSerializer):
    class Meta:
        model = FundLog
        fields = "__all__"


class FundLogView(ListAPIView):
    # permission_classes = [IsAuthenticated, ]
    
    pagination_class = PageNumberPagination
    serializer_class = FundLogSerializer
    queryset = FundLog.objects.order_by("-start_time").all()

    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page') or 1
        page_size = request.query_params.get('page_size') or 10
        keyword = request.query_params.get('keyword') or ''
        if keyword:
            queryset = FundLog.objects.filter(
                name__contains=keyword).order_by('id')
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
