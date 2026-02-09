from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta

from src.apps.rates.services import RateService
from src.apps.rates.selectors import get_rate_with_trend
from src.api.v1.rates.serializers import (
    RateLoadInputSerializer, 
    RateGetInputSerializer, 
    RateDetailSerializer
)
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)

class RateLoadView(GenericAPIView):

    serializer_class = RateLoadInputSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_date = serializer.validated_data['date']
        
        logger.info(f"API Request: Load rates for {target_date}")
        
        service = RateService()
        success = service.load_with_history(target_date)

        if success:
            return Response(
                {"status": "success", "loaded_date": target_date}, 
                status=status.HTTP_201_CREATED
            )
        
        logger.error(f"Failed to load rates for {target_date} via API")
        
        return Response(
            {"status": "error", "message": "External API returned no data"}, 
            status=status.HTTP_502_BAD_GATEWAY
        )


class RateDetailView(GenericAPIView):
    
    serializer_class = RateDetailSerializer

    @extend_schema(parameters=[RateGetInputSerializer])
    def get(self, request, *args, **kwargs):
        input_serializer = RateGetInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        target_date = input_serializer.validated_data['date']
        code = input_serializer.validated_data['code']

        rate, trend, previous_rate = get_rate_with_trend(code, target_date)

        if not rate:
            return Response(
                {"error": "Rate not found. Load data first."}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        context = {
            "request": request,
            "trend": trend,
            "previous_rate": previous_rate
        }
        
        serializer = self.get_serializer(rate, context=context)
        
        return Response(serializer.data)