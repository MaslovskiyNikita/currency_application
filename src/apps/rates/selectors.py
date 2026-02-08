from datetime import date
from typing import Optional, Tuple
from src.apps.rates.models import Rate

def get_rate_with_trend(currency_code: str, target_date: date) -> Tuple[Optional[Rate], Optional[str], Optional[Rate]]:

    current_rate = Rate.objects.select_related('currency').filter(
        currency__abbreviation__iexact=currency_code,
        date=target_date
    ).first()

    if not current_rate:
        return None, None, None

    previous_rate = Rate.objects.filter(
        currency=current_rate.currency,
        date__lt=target_date
    ).order_by('-date').first()

    trend = "stable"
    if previous_rate:
        if current_rate.official_rate > previous_rate.official_rate:
            trend = "up"
        elif current_rate.official_rate < previous_rate.official_rate:
            trend = "down"
    else:
        trend = None

    return current_rate, trend, previous_rate