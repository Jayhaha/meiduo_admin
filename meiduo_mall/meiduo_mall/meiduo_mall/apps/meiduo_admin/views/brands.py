from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import Brand
from meiduo_admin.serializers.brands import BrandsSerializer


class BrandsViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    # 指定视图使用的查询集
    queryset = Brand.objects.all()
    # 指定视图使用的序列化器类
    serializer_class = BrandsSerializer
