from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.permissions import PermissionSerializer, ContentTypeSerializer, PermissionGroupSerializer, \
    PermissionSimpleSerializer, PermissionAdminSerializer, PermissionSimpleGroupSerializer

from users.models import User


# 保存权限表数据
# POST /meiduo_admin/permission/perms/

# 删除权限表数据
# DELETE /meiduo_admin/permission/perms/(?P<pk>\d+)/

# 修改指定权限表数据
#  PUT /meiduo_admin/permission/perms/(?P<pk>\d+)/
class PermissionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    serializer_class = PermissionSerializer

    queryset = Permission.objects.all()

    # 获取权限内容类型列表数据
    # GET /meiduo_admin/permission/content_types/
    def content_types(self, request):
        """
        获取权限内容
        1.获取权限内容
        2.序列化返回
        """
        res = ContentType.objects.all()
        serializer = ContentTypeSerializer(res, many=True)

        return Response(serializer.data)


class PermissionGroupsViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    serializer_class = PermissionGroupSerializer

    queryset = Group.objects.all()

    def simple(self, request):
        """获取权限简单数据"""
        res = Permission.objects.all()

        serializer = PermissionSimpleSerializer(res, many=True)

        return Response(serializer.data)


class PerssionsAdminViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    serializer_class = PermissionAdminSerializer

    queryset = User.objects.filter(is_staff=True)

    def simple(self, request):
        res = Group.objects.all()
        serializer = PermissionSimpleGroupSerializer(res, many=True)
        return Response(serializer.data)


#保存管理员数据
# POST /meiduo_admin/permission/admins/

