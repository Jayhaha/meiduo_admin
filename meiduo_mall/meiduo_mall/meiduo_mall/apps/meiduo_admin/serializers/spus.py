from rest_framework import serializers

from goods.models import SPU, SpecificationOption, SPUSpecification, SKU, Brand, GoodsCategory


class SPUSimpleSerializer(serializers.ModelSerializer):
    """SPU序列化器类"""

    class Meta:
        model = SPU
        fields = ('id', 'name')


class SpecOptionSerializer(serializers.ModelSerializer):
    """SPU规格序列化器类"""

    class Meta:
        model = SpecificationOption
        fields = ('id', 'value')


class SPUSpecSerializer(serializers.ModelSerializer):
    """SPU规格序列化器类"""
    # 关联对象的嵌套序列化
    options = SpecOptionSerializer(label='Opt选项', many=True)

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'options')









class SPUSerializer(serializers.ModelSerializer):
    """SPU序列化器类"""

    brand =serializers.StringRelatedField(label='品牌名称')
    brand_id = serializers.IntegerField(label='品牌ID')

    category1_id = serializers.IntegerField(label='一级分类id')
    category2_id = serializers.IntegerField(label='二级分类id')
    category3_id = serializers.IntegerField(label='二级分类id')

    category1 = serializers.StringRelatedField(label='一级分类id')
    category2 = serializers.StringRelatedField(label='二级分类id')
    category3 = serializers.StringRelatedField(label='二级分类id')

    class Meta:
        model = SPU
        exclude = ('create_time','update_time')


    # def create(self, validated_data):





class SPUBrandsSimpleSerializer(serializers.ModelSerializer):
    """商品品牌序列化器类"""

    class Meta:
        model = Brand
        fields = ('id','name')


class SPUOneSerializer(serializers.ModelSerializer):
   """一级分类"""

   class Meta:
       model = GoodsCategory
       fields = ('id','name')


class SPUTwoSerializer(serializers.ModelSerializer):
    """二级分类"""
    subs = SPUOneSerializer(label='弟弟', many = True)


    class Meta:
        model = GoodsCategory
        fields = ('id','name','subs')


# class SPUImageSerializer(serializers.ModelSerializer):
#     """SPU图片序列化器类"""
#     res =


