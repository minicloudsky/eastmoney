from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.log import serializers
from apps.log.models import Log


class LogView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.LogSerializer
    queryset = Log.objects.order_by("-create_time").all()

    def list(self, request, *args, **kwargs):
        keyword = request.query_params.get("keyword", "")
        if keyword:
            queryset = Log.objects.filter(api_name__contains=keyword).order_by('id')
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
