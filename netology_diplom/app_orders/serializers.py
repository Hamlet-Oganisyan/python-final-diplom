from rest_framework import serializers
from .models import Order, OrderItem
from app_shops.serializers import ProductInfoSerializer
from app_users.serializers import ContactSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('id',)
        # extra_kwargs = {
        #     'order': {'write_only': True}
        # }


class OrderItemCreateSerializer(OrderItemSerializer):
    product_info = ProductInfoSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemCreateSerializer(read_only=True, many=True)
    total_sum = serializers.IntegerField()
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id',)