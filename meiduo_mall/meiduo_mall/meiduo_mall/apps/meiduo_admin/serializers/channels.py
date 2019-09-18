from rest_framework import serializers

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory


class ChannelSerializer(serializers.ModelSerializer):
    """频道序列化器类"""
    #因为这里我们要的是名称不是我们外键对象,所以我们用StringRelatedField字段显示
    # 指定对应模型类STR方法的返回值,就是对应的名称
    category = serializers.StringRelatedField(label='一级分类名称')
    group = serializers.StringRelatedField(label='频道组名称')


    category_id = serializers.IntegerField(label='一级分类ID')
    group_id = serializers.IntegerField(label='频道组ID')

    class Meta:
        model = GoodsChannel
        exclude = ('create_time', 'update_time')


    def validate_category_id(self,value):
        #一级分类是否存在
        try:
            GoodsCategory.objects.get(id = value,parent=None)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('一级分类不存在')
        return value

    def validate_group_id(self, value):
        # 频道组是否存在
        try:
            GoodsChannelGroup.objects.get(id=value)
        except GoodsChannelGroup.DoesNotExist:
            raise serializers.ValidationError('频道组不存在')

        return value



class ChannelGroupSerializer(serializers.ModelSerializer):
    """频道组序列化器类"""
    class Meta:
        model = GoodsChannelGroup
        #因为原模型类继承了basemodel所以我们这里需要指定
        fields = ('id','name')



class ChannelCategorySerializer(serializers.ModelSerializer):
    """获取一级分类序列化器"""

    class Meta:
        model = GoodsCategory
        fields = ('id','name')






