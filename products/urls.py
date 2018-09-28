from django.urls import path

from .views import (
    ProductListView,
    ProductListFeaturedView,
    ProductDetailView,
    ProductDetailFeaturedView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product'),
    path('featured/', ProductListFeaturedView.as_view(), name='product'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('featured/<int:pk>/', ProductDetailFeaturedView.as_view(), name='product-detail'),
]
