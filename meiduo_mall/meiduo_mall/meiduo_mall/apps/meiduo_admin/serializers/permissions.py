from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from users.models import User


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypeSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(label='权限内容类型名称')

    class Meta:
        model = ContentType
        fields = ('id', 'name')


class PermissionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name')


class PermissionAdminSerializer(serializers.ModelSerializer):
    # username = serializers.StringRelatedField(label='用户名')

    class Meta:
        model = User

        fields = ('id', 'username', 'email', 'mobile', 'password', 'user_permissions', 'groups')
        # fields = '__all__'

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
                'allow_blank': True
            }
        }

    def create(self, validated_data):
        """创建管理员用户"""
        # 设置管理员标记is_staff为True
        validated_data['is_staff'] = True

        # 创建新的管理员用户
        user = super().create(validated_data)

        # 密码加密保存
        password = validated_data['password']

        if not password:
            # 设置管理员默认密码
            password = '123abc'

        user.set_password(password)
        user.save()
        return user

    def update(self,instance, validated_data):
        """修改管理员用户"""
        #从validated_data中取出密码password
        password = validated_data.pop('password',None)
        #修改管理员账户信息,update的操作一定是要传入俩个值,一个是对象一个数据
        super().update(instance,validated_data)

        #修改密码
        if password:
            instance.set_password(password)
            instance.save()
        return instance




class PermissionSimpleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')
