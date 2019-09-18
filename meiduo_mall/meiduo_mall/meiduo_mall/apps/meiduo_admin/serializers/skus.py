from django.db import transaction
from rest_framework import serializers

from goods.models import SKUImage, SKU, SKUSpecification, SPU, SpecificationOption


class SKUImageSerializer(serializers.ModelSerializer):
    """id = IntegerField(label='ID', read_only=True)
    sku_id = IntegerField(label='SKU商品ID')
    sku = StringRelatedField(label='sku商品名称')
    image = ImageField(label='图片', max_length=100)
"""
    """sku图片序列化器类"""
    sku_id = serializers.IntegerField(label='SKU商品ID')
    # 因为通过交互环境创建对象知道我们这里返回的sku 是一个对象,或者说是一个查询集
    # 但是我们这里需要的是sku商品的名称,所以我们是输出str方法的返回值
    sku = serializers.StringRelatedField(label='sku商品名称')

    class Meta:
        model = SKUImage
        exclude = ('create_time', 'update_time')

    def validate_sku_id(self, value):
        # 查看sku商品是否存在
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        return value

    def create(self, validated_data):
        """sku商品上传图片保存"""
        print(validated_data)

        sku_image = super().create(validated_data)

        # 保存上传图片记录
        sku = SKU.objects.get(id=validated_data['sku_id'])

        # 如果sku商品没有默认图片,则设置其为默认图片
        if not sku.default_image:
            sku.default_image = sku_image.image
            sku.save()
        return sku_image


class SKUSimpleSerializer(serializers.ModelSerializer):
    """SKU商品序列化器类"""

    class Meta:
        model = SKU
        fields = ('id', 'name')


class SKUSpecSerializer(serializers.ModelSerializer):
    """SPEC商品规格序列化器类"""
    spec_id = serializers.IntegerField(label='规格ID')
    option_id = serializers.IntegerField(label='选项ID')

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSerializer(serializers.ModelSerializer):
    """SKU商品序列化器类"""

    spu_id = serializers.IntegerField(label='SPU编号')
    category = serializers.StringRelatedField(label='三级分类名称')

    # 关联对象嵌套序列化
    specs = SKUSpecSerializer(label='商品规格信息', many=True)

    class Meta:
        model = SKU
        exclude = ('create_time', 'update_time', 'default_image', 'spu', 'comments')
        extra_kwargs = {
            'sales': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        # 获取spu_id
        spu_id = attrs['spu_id']
        # 检查spu商品是否存在
        try:
            spu = SPU.objects.get(id=spu_id)
        except SPU.DoesNotExist:
            raise serializers.ValidationError('SPU商品不存在')

        # attrs中添加第三级分类ID
        attrs['category_id'] = spu.category3.id

        # 检查sku规格数据是否有效
        specs = attrs['specs']
        spu_specs = spu.specs.all()
        spec_count = spu_specs.count()

        # SKU商品的规格数据是否完整
        if spec_count != len(specs):
            raise serializers.ValidationError('SKU规格数据不完整')

        # SKU商品的规格数据是否一致
        specs_ids = [spec.get('spec_id') for spec in specs]
        spu_specs_ids = [spec.id for spec in spu_specs]

        # 排序
        specs_ids.sort()
        spu_specs_ids.sort()

        # 对比规格数据是否一致
        if spu_specs_ids != specs_ids:
            raise serializers.ValidationError('商品规格数据有误')

        for spec in specs:
            spec_id = spec.get('spec_id')
            option_id = spec.get('option_id')

            # 检查spec_id对应的规格是否包含option_id对应的选项
            options = SpecificationOption.objects.filter(spec_id=spec_id)
            options_ids = [option.id for option in options]

            if option_id not in options_ids:
                raise serializers.ValidationError('规格选项数据有误')

        return attrs

    def create(self, validated_data):
        """保存sku商品数据"""
        specs = validated_data.pop('specs')

        with transaction.atomic():
            # 新增sku商品
            sku = SKU.objects.create(**validated_data)
            # sku = super().create(**validated_data)
            # return sku

            # 保存商品规格信息
            for spec in specs:
                SKUSpecification.objects.create(
                    sku=sku,
                    spec_id=spec.get('spec_id'),
                    option_id=spec.get('option_id')
                )

        return sku

    def update(self, instance, validated_data):
        """修改sku商品数据"""
        specs = validated_data.pop('specs')
        with transaction.atomic():
            # 调用父类方法更新sku商品.回顾3种方式
            # 1.父类名加方法名
            # 2.super(本类名,对象).方法()
            # 3.super().方法名()
            sku = super().update(instance, validated_data)

            # 清除sku原有的规格信息
            instance.specs.all().delete()

            # 保存商品规格信息
            for spec in specs:
                SKUSpecification.objects.create(
                    sku=instance,
                    spec_id=spec.get('spec_id'),
                    option_id=spec.get('option_id')
                )
        return sku
