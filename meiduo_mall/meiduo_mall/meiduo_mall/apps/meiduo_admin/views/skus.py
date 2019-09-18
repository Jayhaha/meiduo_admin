from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from goods.models import SKUImage, SKU, SPU

# sku图片的获取
# 请求参数:通过请求头传递jwt_token数据
# GET  /meiduo_admin/skus/images/?page=<页码>&page_size=<页容量>
from meiduo_admin.serializers.skus import SKUImageSerializer, SKUSimpleSerializer, SKUSerializer


class SKUImageViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    serializer_class = SKUImageSerializer
    queryset = SKUImage.objects.all()



"""
请求方式： GET /meiduo_admin/skus/simple/

请求参数： 通过请求头传递jwt token数据。

返回数据： JSON

    [
        {
            "id": "sku商品ID",
            "name": "sku商品名称",
        },
        ...
    ]
"""


# 获取SKU商品简单数据
# GET /meiduo_admin/skus/simple/
class SKUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SKUSimpleSerializer
    queryset = SKU.objects.all()
    pagination_class = None


#获取SKU表数据

class SKUViewSet(ModelViewSet):
    """SKU视图集"""
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    def get_queryset(self):
        """获取当前视图所使用的查询集"""
        keyword = self.request.query_params.get('keyword')

        if keyword:
            skus = SKU.objects.filter(Q(name__contains=keyword) |
                                      Q(caption__contains=keyword))


        else:
            skus = SKU.objects.all()

        return skus
    #指定序列化器类
    serializer_class = SKUSerializer





