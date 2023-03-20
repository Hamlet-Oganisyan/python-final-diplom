from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PartnerUpdate, CategoryView, ShopView, ProductInfoView, PartnerState

app_name = 'app_shops'

router = DefaultRouter()
router.register(r'shop', ShopView, basename='shop')
router.register(r'category', CategoryView, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('partner/state', PartnerState.as_view(), name='partner-state'),
    path('products', ProductInfoView.as_view(), name='shops'),
    ]
