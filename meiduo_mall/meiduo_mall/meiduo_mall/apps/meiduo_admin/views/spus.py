# GET /meiduo_admin/goods/simple/
from django.conf import settings
from django.views import View
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from goods.models import SPU, SPUSpecification, GoodsCategory, Brand
from meiduo_admin.serializers.spus import SPUSimpleSerializer, SPUSpecSerializer, SPUSerializer, \
    SPUBrandsSimpleSerializer, SPUOneSerializer, SPUTwoSerializer
from meiduo_mall.utils.fdfs.storage import FDFSStorage


class SPUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    # 指定视图使用的查询集
    queryset = SPU.objects.all()
    # 指定视图使用的序列化器类
    serializer_class = SPUSimpleSerializer

    # 注：关闭分页
    pagination_class = None


"""
2. 获取SPU商品规格信息
2.1 接口设计
请求方式： GET /meiduo_admin/goods/(?P<pk>\d+)/specs/

请求参数： 通过请求头传递jwt token数据。

在路径中传递当前SPU商品id
"""

"""
class SPUSpecView(GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
       
        # 获取spu规格选项数据:
        # 1. 根据pk获取spu specs数据
        # 2. 将spu数据序列化并返回
        
        # 1. 根据pk获取spu specs数据
        specs = SPUSpecification.objects.filter(spu_id=pk)

        # 2. 将spu数据序列化并返回
        serializer = SPUSpecSerializer(specs, many=True)
        return Response(serializer.data)
"""


class SPUSpecView(ListAPIView):
    permission_classes = [IsAdminUser]

    # 指定序列化器类
    serializer_class = SPUSpecSerializer

    def get_queryset(self):
        """返回视图所使用的查询集"""
        # 获取pk
        pk = self.kwargs['pk']
        return SPUSpecification.objects.filter(spu_id=pk)

    # 注：关闭分页
    pagination_class = None


class SPUViewSet(ModelViewSet):
    """频道管理视图集"""
    permission_classes = [IsAdminUser]

    lookup_value_regex = '\d+'
    # 指定视图所使用的查询集
    queryset = SPU.objects.all()
    # 指定序列化器类
    serializer_class = SPUSerializer

    def simple(self, request):
        queryset = Brand.objects.all()
        # 指定视图使用的序列化器类
        serializer = SPUBrandsSimpleSerializer(queryset, many=True)

        # 注：关闭分页
        # pagination_class = None
        return Response(serializer.data)

    def image(self, request):
        image = request.FILES.get('image')
        # print(image)
        # return image
        if image is None:
            return Response('上传图片失败')

        image_url = FDFSStorage()._save(name=image, content=image)
        url = settings.FDFS_URL + image_url

        data = {
            'img_url': url
        }

        return Response(data)


# def get_queryset(self):
#     queryset = GoodsCategory.objects.filter(parent=None)
#     serializer= SPUOneSerializer(queryset,many=True)
#
#     return Response(serializer.data)


# class SPUBrandsSimpleView(ListAPIView):
#     permission_classes = [IsAdminUser]
#     # 指定视图使用的查询集
#     queryset = Brand.objects.all()
#     # 指定视图使用的序列化器类
#     serializer_class = SPUBrandsSimpleSerializer
#
#     # 注：关闭分页
#     pagination_class = None


class SPUCategoriesView(ListAPIView):
    permission_classes = [IsAdminUser]
    # 指定视图使用的序列化器类
    serializer_class = SPUOneSerializer

    # 指定视图使用的查询集
    def get_queryset(self):
        queryset = GoodsCategory.objects.filter(parent=None)
        return queryset

    # 注：关闭分页
    pagination_class = None


class SPUTwoView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    # 指定视图使用的序列化器类
    serializer_class = SPUTwoSerializer

    # 指定视图使用的查询集
    def get_object(self):
        pk = self.kwargs['pk']
        categorys = GoodsCategory.objects.get(id=pk)

        querysets = GoodsCategory.objects.filter(parent=pk)

        categorys.subs = [category for category in querysets]

        return categorys

    # 注：关闭分页
    pagination_class = None

    # POST /meiduo_admin/goods/images/

# class SPUGoodsImages(APIView):
#     permission_classes = [IsAdminUser]
#
#     def post(self,request):
#         image = request.FILES.get('image')
#         # print(image)
#         # return image
#         if image is None:
#             return Response('上传图片失败')
#
#         image_url = FDFSStorage()._save( name=image, content=image)
#         url = settings.FDFS_URL + image_url
#
#         data = {
#             'img_url':url
#         }
#
#         return Response(data)
