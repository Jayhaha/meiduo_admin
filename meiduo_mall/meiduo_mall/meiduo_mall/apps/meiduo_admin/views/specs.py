from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from goods.models import SPUSpecification, SpecificationOption
from meiduo_admin.serializers.specs import SpecsSerializer, SpecsOptionsSerializer


# 查询获取规格表列表数据
# GET /meiduo_admin/goods/specs/
class SpecsViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SpecsSerializer
    queryset =SPUSpecification.objects.all()



class SpecsOptionsViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SpecsOptionsSerializer
    queryset = SpecificationOption.objects.all()


    def simple(self,request):
        queryset = SPUSpecification.objects.all()
        serializer = SpecsSerializer(queryset,many=True)
        return Response(serializer.data)




# GET /meiduo_admin/goods/specs/simple/
#
# class


