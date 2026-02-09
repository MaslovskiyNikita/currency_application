from rest_framework import serializers
from src.apps.rates.models import Rate


class RateLoadInputSerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])

class RateGetInputSerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    code = serializers.CharField(min_length=3, max_length=3)


class RateDetailSerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(source='currency.code')
    currency_abbreviation = serializers.CharField(source='currency.abbreviation')
    currency_name = serializers.CharField(source='currency.name')
    
    official_rate = serializers.DecimalField(
        max_digits=10,
        decimal_places=4,
        coerce_to_string=False
    )

    trend = serializers.SerializerMethodField()
    previous_official_rate = serializers.SerializerMethodField()
    previous_date = serializers.SerializerMethodField()
    diff = serializers.SerializerMethodField()

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

    def get_trend(self, obj):
        return self.context.get('trend')

    def get_previous_official_rate(self, obj):
        previous_rate = self.context.get('previous_rate')
        if previous_rate:
            return previous_rate.official_rate
        return None

    def get_previous_date(self, obj):
        previous_rate = self.context.get('previous_rate')
        return previous_rate.date if previous_rate else None

    def get_diff(self, obj):
        previous_rate = self.context.get('previous_rate')
        if previous_rate:
            return obj.official_rate - previous_rate.official_rate
        return None