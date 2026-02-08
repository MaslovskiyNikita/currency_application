from django.urls import path
from .views import RateLoadView, RateDetailView

urlpatterns = [
    path('load/', RateLoadView.as_view(), name='rates-load'),
    path('rate/', RateDetailView.as_view(), name='rates-detail'),
]