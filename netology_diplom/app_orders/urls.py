from django.urls import path
from .views import BasketView, OrderView, PartnerOrders

app_name = 'app_orders'

urlpatterns = [
    path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    path('basket', BasketView.as_view(), name='basket'),
    path('order', OrderView.as_view(), name='order'),

]
