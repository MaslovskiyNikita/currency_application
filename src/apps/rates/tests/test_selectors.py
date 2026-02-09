import pytest
from datetime import date
from decimal import Decimal
from src.apps.rates.models import Rate
from src.apps.rates.selectors import get_rate_with_trend

pytestmark = pytest.mark.django_db


@pytest.fixture
def make_rate(currency):
    def _make(target_date, rate_str):
        return Rate.objects.create(
            currency=currency,
            date=target_date,
            official_rate=Decimal(rate_str),
            scale=1
        )
    return _make


def test_returns_none_when_rate_not_found():

    current, trend, previous = get_rate_with_trend("USD", date(2025, 1, 1))
    
    assert current is None
    assert trend is None
    assert previous is None


def test_trend_none_when_no_previous_rate(make_rate):

    make_rate(date(2025, 1, 10), "3.2000")
    
    current, trend, previous = get_rate_with_trend("USD", date(2025, 1, 10))
    
    assert current is not None
    assert trend is None
    assert previous is None


def test_trend_up(make_rate):

    make_rate(date(2025, 1, 9), "3.1000")   
    make_rate(date(2025, 1, 10), "3.2000")  
    
    _, trend, previous = get_rate_with_trend("USD", date(2025, 1, 10))
    
    assert trend == "up"
    assert previous is not None
    assert previous.official_rate == Decimal("3.1000")


def test_trend_down(make_rate):

    make_rate(date(2025, 1, 9), "3.3000")
    make_rate(date(2025, 1, 10), "3.2000")
    
    _, trend, _ = get_rate_with_trend("USD", date(2025, 1, 10))
    
    assert trend == "down"


def test_trend_stable(make_rate):

    make_rate(date(2025, 1, 9), "3.2000")
    make_rate(date(2025, 1, 10), "3.2000")
    
    _, trend, _ = get_rate_with_trend("USD", date(2025, 1, 10))
    
    assert trend == "stable"


def test_case_insensitive_lookup(make_rate):

    make_rate(date(2025, 1, 10), "3.2000")
    
    current, _, _ = get_rate_with_trend("usd", date(2025, 1, 10))
    
    assert current is not None
    assert current.currency.abbreviation == "USD"


def test_previous_rate_found_despite_gap(make_rate):
    
    make_rate(date(2025, 1, 1), "3.0000")
    make_rate(date(2025, 1, 10), "3.2000")
    
    _, trend, previous = get_rate_with_trend("USD", date(2025, 1, 10))
    
    assert previous is not None
    assert previous.date == date(2025, 1, 1)
    assert trend == "up"