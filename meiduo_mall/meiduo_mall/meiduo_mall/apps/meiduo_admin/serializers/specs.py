from rest_framework import serializers

from goods.models import SPUSpecification, SpecificationOption


class SpecsSerializer(serializers.ModelSerializer):

    spu = serializers.StringRelatedField(label='SPU商品名称')
    spu_id = serializers.IntegerField(label='SPU商品ID')


    class Meta:
        model = SPUSpecification
        fields='__all__'


class SpecsOptionsSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField(label='规格id')
    spec = serializers.StringRelatedField(label='规格id')


    class Meta:
        model = SpecificationOption
        fields = '__all__'