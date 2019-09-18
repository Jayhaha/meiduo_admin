from rest_framework import serializers

from goods.models import Brand


class BrandsSerializer(serializers.ModelSerializer):


    class Meta:
        model = Brand
        fields = '__all__'