from rest_framework import serializers

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods


class OrderListSerializer(serializers.ModelSerializer):
    """订单序列化器类"""
    create_time = serializers.DateTimeField(label='创建时间',format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = OrderInfo
        fields = ('order_id','create_time')


class SKUSimpleSerializer(serializers.ModelSerializer):
    """订单商品序列化器类"""
    class Meta:
        model = SKU
        fields = ('id', 'name', 'default_image')


class OrderSKUSerializer(serializers.ModelSerializer):
    """订单商品序列化器类"""
    # 关联对象的嵌套序列化
    sku = SKUSimpleSerializer(label='SKU商品')

    class Meta:
        model = OrderGoods
        fields = ('id', 'count', 'price', 'sku')


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单详情序列化器类"""
    # 关联对象的嵌套序列化
    user = serializers.StringRelatedField(label='下单用户')
    skus = OrderSKUSerializer(label='订单商品', many=True)

    create_time = serializers.DateTimeField(label='下单时间', format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = OrderInfo
        exclude = ('update_time', 'address')


class OrderStatusSerializer(serializers.ModelSerializer):
    """订单状态序列化器类"""
    class Meta:
        model = OrderInfo
        fields = ('order_id', 'status')
        extra_kwargs = {
            'order_id':{
                'read_only':True

            }
        }
    def validate_status(self,value):
        if value not in [1,2,3,4,5,6]:
            raise serializers.ValidationError('订单状态有误')
        return value
