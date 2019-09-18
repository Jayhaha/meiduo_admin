from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory
from meiduo_admin.serializers.channels import ChannelSerializer, ChannelGroupSerializer, ChannelCategorySerializer


# /meiduo_admin/goods/channels/(?P<pk>\d+)
#展示商品分类表,满足目前的增删改查
class ChannelViewSet(ModelViewSet):
    """频道管理视图集"""
    permission_classes = [IsAdminUser]
    # 指定视图所使用的查询集
    queryset = GoodsChannel.objects.all()
    # 指定序列化器类
    serializer_class = ChannelSerializer


#1. 获取频道组数据
# GET /meiduo_admin/goods/channel_types/
class ChannelTypesView(ListAPIView):
    """频道组视图"""
    permission_classes = [IsAdminUser]
    # 指定视图所使用的查询集
    queryset = GoodsChannelGroup.objects.all()

    # 指定序列化器类
    serializer_class = ChannelGroupSerializer

    # 注：关闭分页
    pagination_class = None

# 2.获取一级分类数据
# GET /meiduo_admin/goods/categories/
class ChannelCategoriesView(ListAPIView):
    """频道对应一级分类视图"""
    permission_classes = [IsAdminUser]
    # 指定视图所使用的查询集
    queryset = GoodsCategory.objects.filter(parent=None)
    # 指定序列化器类
    serializer_class = ChannelCategorySerializer

    # 注：关闭分页
    pagination_class = None

#3.保存新增频道数据
# 就是我们的第一个借口的增删改查.所以可以直接用




