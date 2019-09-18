from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from meiduo_admin.serializers.users import AdminAuthSerializer, UserSerializer

# POST /meiduo_admin/authorizations/
from users.models import User


class AdminAuthorizeView(CreateAPIView):
    serializer_class = AdminAuthSerializer

    # def post(self, request):
    #     """
    #            管理员登录:
    #            1. 获取参数并进行校验
    #            2. 服务器签发jwt token数据
    #            3. 返回应答
    #            """
    #     # 1. 获取参数并进行校验
    #     serializer = AdminAuthSerializer(data = request.data)
    #     serializer.is_valid(raise_exception = True)
    #
    #     # 2. 服务器签发jwt token数据(create)
    #     serializer.save()
    #
    #     # 3. 返回应答
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# GET /meiduo_admin/users/?keyword=<搜索内容>&page=<页码>&pagesize=<页容量>
class UserInfoView(ListAPIView):
    permission_classes = [IsAdminUser]
    # 指定视图所使用的序列化器类
    serializer_class = UserSerializer

    # def get(self, request):
    #     """
    #     获取普通用户数据
    #     1. 获取keyword关键字
    #     2. 查询普通用户数据
    #     3. 将用户数据序列化并返回
    #     """
    #     # 1.获取keyword关键字
    #     # 这里是查询字符串传参,request.query_params
    #     # 如果是请求体传参那就是,request.data === request.GET类似
    #
    #     keyword = request.query_params.get('keyword')
    #
    #     # 2.查询普通用户数据
    #     # username__contains意思是:username这个名字中,包含keyword某个词部分
    #     # contains模糊查询
    #     #
    #     #
    #     # 存在keyword的时候,显示查询的username的数据,不存在keyword的时候返回除了管理员之外的用户
    #     if keyword:
    #         users = User.objects.filter(is_staff=False, username__contains=keyword)
    #     else:
    #         users = User.objects.filter(is_staff=False)
    #
    #     # 3.将用户数据序列化并返回
    #     # email,username在继承的父类中AbstractUser已经被检验
    #     # mobile
    #     serializer = UserSerializer(users,many=True)
    #     return Response(serializer.data)

    def get_queryset(self):
        """返回视图所使用的查询集"""
        # 1. 获取keyword关键字
        keyword = self.request.query_params.get('keyword')

        # 2. 查询普通用户数据
        if keyword:
            users = User.objects.filter(is_staff=False, username__contains=keyword)
        else:
            users = User.objects.filter(is_staff=False)

        return users


    # def get(self, request):ListAPIView
    #     """
    #     获取普通用户数据:
    #     1. 获取keyword关键字
    #     2. 查询普通用户数据
    #     3. 将用户数据序列化并返回
    #     """
    #     # 查询普通用户数据
    #     users = self.get_queryset()
    #
    #     # 3. 将用户数据序列化并返回
    #     serializer = self.get_serializer(users, many=True)
    #     return Response(serializer.data)

    # POST /meiduo_admin/users/
    def post(self,request):
        """
       新增用户数据:
       1. 获取参数并进行校验
       2. 创建并保存新用户数据
       3. 将新用户数据序列化并返回

       因为是新增用户,所以肯定是请求体传参
       这里的获得数据一定是request.data
       """
        # 1. 获取参数并进行校验
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        # 2. 创建并保存新用户数据
        serializer.save()

        # 3. 将新用户数据序列化并返回
        return Response(serializer.data,status.HTTP_201_CREATED)




