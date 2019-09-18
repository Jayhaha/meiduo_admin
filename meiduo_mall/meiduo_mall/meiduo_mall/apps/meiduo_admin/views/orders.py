from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet

from meiduo_admin.serializers.orders import OrderListSerializer, OrderDetailSerializer, OrderStatusSerializer
from orders.models import OrderInfo


class OrdersViewSet(UpdateModelMixin,ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = OrderListSerializer

    def get_serializer_class(self):
        """返回视图所使用的序列化器类"""
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderStatusSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')

        if keyword:
            orders = OrderInfo.objects.filter(skus__sku__name__contains=keyword).distinct()
        else:
            orders = OrderInfo.objects.all()
        return orders

        # PUT /meiduo_admin/orders/(?P<pk>\d+)/status/

    @action(methods=['put'], detail=True)
    def status(self, request, pk):
        """
        修改订单状态:
        1. 校验订单是否有效
        2. 获取订单状态status并校验(status必传，status是否合法)
        3. 修改并保存订单的状态
        4. 返回应答
        """
        # # 1. 校验订单是否有效
        # order = self.get_object()
        #
        # # 2. 获取订单状态status并校验(status必传，status是否合法)
        # serializer = OrderStatusSerializer(order, data=request.data)
        # serializer.is_valid(raise_exception=True)
        #
        # # 3. 修改并保存订单的状态
        # serializer.save()

        # 4. 返回应答
        # return Response(serializer.data)
        return self.update(request,pk)

