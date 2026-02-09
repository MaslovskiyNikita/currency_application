import pytest
from datetime import date
from decimal import Decimal
from src.apps.rates.models import Rate
from src.apps.rates.services import RateService

pytestmark = pytest.mark.django_db

@pytest.fixture
def service_with_mock(mocker):

    def _make(rates_return):

        mock_cls = mocker.patch("src.apps.rates.services.NBRBClient")
        mock_instance = mock_cls.return_value.__enter__.return_value
        mock_instance.get_rates_on_date.side_effect = [rates_return, []]
        
        return RateService()

    return _make


def test_load_with_history_creates_rates(service_with_mock, make_dto, currency):

    service = service_with_mock([make_dto(official_rate="3.2000")])
    result = service.load_with_history(date(2025, 1, 10))

    assert result is True
    rate = Rate.objects.get(date=date(2025, 1, 10), currency=currency)
    assert rate.official_rate == Decimal("3.2000")


def test_load_with_history_returns_false_on_empty(service_with_mock):

    service = service_with_mock([]) 
    
    result = service.load_with_history(date(2025, 1, 10))

    assert result is False
    assert Rate.objects.count() == 0


def test_load_with_history_updates_on_conflict(service_with_mock, make_dto, currency):

    Rate.objects.create(
        currency=currency,
        date=date(2025, 1, 10),
        scale=1,
        official_rate=Decimal("3.0000"),
    )

    service = service_with_mock([make_dto(official_rate="3.5000")])
    service.load_with_history(date(2025, 1, 10))

    rate = Rate.objects.get(currency=currency, date=date(2025, 1, 10))
    assert rate.official_rate == Decimal("3.5000")


def test_load_with_history_skips_unknown_currencies(service_with_mock, make_dto):

    service = service_with_mock([make_dto(cur_id=9999)])
    
    result = service.load_with_history(date(2025, 1, 10))

    assert result is True 
    assert Rate.objects.count() == 0 