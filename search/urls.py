from django.urls import path

from .views import (
    SearchProductView,
)


urlpatterns = [
    path('search/', SearchProductView.as_view(), name='query')
]