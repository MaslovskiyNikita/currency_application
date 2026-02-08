from django.urls import path, include

urlpatterns = [
    path('rates/', include('src.api.v1.rates.urls')),
]