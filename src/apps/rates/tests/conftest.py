import pytest
from datetime import date
from decimal import Decimal
from src.apps.rates.models import Currency
from src.apps.integrations.nbrb.dto import NBRBRateDTO

@pytest.fixture
def currency(db):

    return Currency.objects.create(
        nbrb_id=431,
        code="840",
        abbreviation="USD",
        name="Доллар США",
    )

@pytest.fixture
def make_dto():

    def _make(
        cur_id=431,
        date=date(2025, 1, 10),
        abbreviation="USD",
        scale=1,
        name="Доллар США",
        official_rate="3.2000",
        **kwargs
    ):

        if 'rate' in kwargs:
            official_rate = kwargs['rate']

        return NBRBRateDTO(
            cur_id=cur_id,
            date=date,
            abbreviation=abbreviation,
            scale=scale,
            name=name,
            official_rate=Decimal(str(official_rate))
        )
    return _make