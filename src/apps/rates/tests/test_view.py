import pytest
from datetime import date
from decimal import Decimal
from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from src.apps.rates.models import Rate


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


def test_load_success(api_client):
    url = reverse("rates-load")  
    
    with patch(
        "src.apps.rates.services.RateService.load_with_history", return_value=True
    ) as mock_load:
        response = api_client.post(
            url,
            {"date": "2025-01-10"},
            format="json",
        )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == "success"

    mock_load.assert_called_once_with(date(2025, 1, 10))


def test_load_failure_returns_502(api_client):
    url = reverse("rates-load")
    
    with patch(
        "src.apps.rates.services.RateService.load_with_history", return_value=False
    ):
        response = api_client.post(
            url,
            {"date": "2025-01-10"},
            format="json",
        )

    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    assert response.data["status"] == "error"


def test_load_invalid_date_returns_400(api_client):
    url = reverse("rates-load")
    response = api_client.post(url, {"date": "not-a-date"}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_load_missing_date_returns_400(api_client):
    url = reverse("rates-load")
    response = api_client.post(url, {}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST



def test_rate_not_found(api_client):
    url = reverse("rates-detail")
    response = api_client.get(
        url,
        {"date": "2025-01-10", "code": "USD"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    

def test_rate_found_without_previous(api_client, currency):
    Rate.objects.create(
        currency=currency,
        date=date(2025, 1, 10),
        scale=1,
        official_rate=Decimal("3.2000"),
    )
    
    url = reverse("rates-detail")
    response = api_client.get(
        url,
        {"date": "2025-01-10", "code": "USD"},
    )

    assert response.status_code == status.HTTP_200_OK
    
    data = response.data
    assert data["currency_code"] == "840"
    assert data["official_rate"] == Decimal("3.2000")
    assert data["trend"] is None
    assert data["previous_official_rate"] is None
    assert data["diff"] is None
    
    assert "X-Response-Signature" in response.headers


def test_rate_found_with_trend_up(api_client, currency):

    Rate.objects.create(
        currency=currency,
        date=date(2025, 1, 9),
        scale=1,
        official_rate=Decimal("3.1000"),
    )

    Rate.objects.create(
        currency=currency,
        date=date(2025, 1, 10),
        scale=1,
        official_rate=Decimal("3.2000"),
    )
    
    url = reverse("rates-detail")
    response = api_client.get(
        url,
        {"date": "2025-01-10", "code": "USD"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.data

    assert data["trend"] == "up"
    assert data["diff"] == Decimal("0.1000")


def test_detail_missing_params_returns_400(api_client):
    url = reverse("rates-detail")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST