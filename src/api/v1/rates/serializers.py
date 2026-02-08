from rest_framework import serializers
from src.apps.rates.models import Rate

class RateLoadInputSerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])

class RateGetInputSerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    code = serializers.CharField(min_length=3, max_length=5)

class RateDetailSerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(source='currency.code')
    currency_abbreviation = serializers.CharField(source='currency.abbreviation')
    currency_name = serializers.CharField(source='currency.name')
    
    trend = serializers.CharField(read_only=True)
    
    
    official_rate = serializers.DecimalField(
        max_digits=10,
        decimal_places=4,
        coerce_to_string=False 
    )
    
    previous_official_rate = serializers.DecimalField(
        max_digits=10, 
        decimal_places=4, 
        read_only=True, 
        allow_null=True
    )

    previous_date = serializers.DateField(read_only=True, allow_null=True)

    diff = serializers.DecimalField(
        max_digits=10, 
        decimal_places=4, 
        read_only=True, 
        allow_null=True
    )

    class Meta:
        model = Rate
        fields = [
            'currency_code', 
            'currency_abbreviation', 
            'currency_name', 
            'date', 
            'official_rate', 
            'scale', 
            'trend',
            'previous_official_rate',
            'previous_date',
            'diff'
        ]