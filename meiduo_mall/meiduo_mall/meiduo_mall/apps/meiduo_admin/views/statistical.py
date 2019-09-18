from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import GoodsVisitCount
from meiduo_admin.serializers.statistical import GoodsVisitSerializer
from orders.models import OrderInfo
from users.models import User

"""
API: GET /meiduo_admin/statistical/total_count/
参数: 
	通过请求头`Authorization`传递jwt token
	格式：Authorization: jwt <jwt token>
响应:
	{
		"count": "网站用户总数",
		"date": "年-月-日"
	}
"""


class UserTotalCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取网站总用户数:
        1. 获取网站总用户数量
        2. 返回应答
        """
        # 1.获取网站总用户数量
        now_date = timezone.now()
        count = User.objects.count()

        # 2.返回答应
        response_data = {
            # date: 只返回`年-月-日`
            'date': now_date.date(),
            'count': count
        }
        return Response(response_data)


"""
API: GET /meiduo_admin/statistical/day_increment/
参数:
	通过请求头`Authorization`传递jwt token
	格式：Authorization: jwt <jwt token>
响应:
	{
		"count": "网站日增用户数",
		"date": "年-月-日"
	}
"""


class UserDayIncrementView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取日增用户数量:
        1. 获取日增用户数量
        2. 返回应答
        """
        # 1.获取日增用户数量
        # replace的作用就是把时间回归到今日的0时0分0秒
        now_date = timezone.now().replace(hour=0, minute=0, second=0)
        count = User.objects.filter(date_joined__gte=now_date).count()

        # 2.返回应答
        response_data = {
            "count": count,
            "date": now_date.date()
        }
        return Response(response_data)


# GET /meiduo_admin/statistical/day_active/
class UserDayActiveView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取日活用户量:
        1. 获取日活用户量
        2. 返回应答
        """
        # 1. 获取日活用户量
        now_date = timezone.now().replace(hour=0, minute=0, second=0)
        count = User.objects.filter(last_login__gte=now_date).count()

        # 2.返回应答
        response_data = {
            "count": count,
            "date": now_date.date()

        }
        return Response(response_data)


# GET /meiduo_admin/statistical/day_orders/
class UserDayOrdersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取日下单用户数量：
        1. 获取日下单用户数量
        2. 返回应答
        """
        # 1. 获取日下单用户数量
        # orders__create_time === User.orders.create_time
        #
        now_date = timezone.now().replace(hour=0, minute=0, second=0)
        count = User.objects.filter(orders__create_time__gte=now_date).distinct().count()

        # **复杂一点的方法.不过容易理解
        # count1 = OrderInfo.objects.filter(create_time__gte=now_date)
        # a = []
        # for i in count1:
        #     b = i.user
        #     if b not in a:
        #         a.append(b)
        # count = len(a)
        # print(count)

        # 2. 返回应答
        response_data = {
            "count": count,
            "date": now_date.date()
        }

        return Response(response_data)


# GET /meiduo_admin/statistical/month_increment/
class UserMonthCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取当月每日新增用户数据:
        1. 获取当月每日新增用户数据
        2. 返回应答
        """
        # 1. 获取当月每日新增用户数据
        # 结束时间
        now_date = timezone.now().replace(hour=0, minute=0, second=0)
        # 起始时间 now_date - 29天
        begin_date = now_date + timezone.timedelta(days=-29)
        # 1.获取当月每日新增用户数据
        data_dict = []
        while True:
            if begin_date <= now_date:
                next_date = begin_date + timezone.timedelta(days=1)
                count = User.objects.filter(date_joined__gte=begin_date,
                                            date_joined__lt=next_date).count()
                data_dict.append({
                    "count": count,
                    "date": begin_date.date()
                })
                begin_date += timezone.timedelta(days=1)
            else:
                break

        # 2.返回应答
        return Response(data_dict)


# GET /meiduo_admin/statistical/goods_day_views/
class GoodsDayView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取当日分类商品访问量：
        1. 查询获取当日分类商品访问量
        2. 将查询数据序列化并返回
        """
        # 1. 查询获取当日分类商品访问量
        # 当前日期
        now_date = timezone.now().date()
        print(now_date)
        # 当日开始时间
        # begin_date = now_date.replace(hour=0, minute=0, second=0)

        # 因为GoodsVisitCount里面保存的date字段格式本来就是年月日
        # 所以不需要判断这个段时间:date__gte=begin_date,date__lt = now_date
        # 直接date = now_date
        goods_visit = GoodsVisitCount.objects.filter(date=now_date)

        # goods_visit_list = []
        # for i in goods_visit:
        #     # category = i.category
        #     goods_visit_list.append({
        #         "category":i.category.name,
        #         "count":i.count
        #     })
        # return Response(goods_visit_list)


        # 2. 将查询数据序列化并返回
        serializer = GoodsVisitSerializer(goods_visit, many=True)
        return Response(serializer.data)
