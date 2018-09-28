from django.urls import path

from .views import (
    ProductListView,
    ProductListFeaturedView,
    ProductDetailView,
    ProductDetailFeaturedView
)

urlpatterns = [
    path('', ProductListFeaturedView.as_view(), name='product'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail')
]
