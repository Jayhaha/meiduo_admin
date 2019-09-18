from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from meiduo_admin.views import users, statistical, channels, skus, spus, orders, permissions, specs, brands

urlpatterns = [
    # 进行url配置
    url(r'^authorizations/$', users.AdminAuthorizeView.as_view()),
    url(r'^statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    url(r'^statistical/day_increment/$', statistical.UserDayIncrementView.as_view()),
    url(r'^statistical/day_active', statistical.UserDayActiveView.as_view()),
    url(r'^statistical/day_orders', statistical.UserDayOrdersView.as_view()),
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    url(r'^statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),
    url(r'^users/$', users.UserInfoView.as_view()),

    url(r'^goods/channel_types/$', channels.ChannelTypesView.as_view()),
    # 频道管理
    url(r'^goods/categories/$', channels.ChannelCategoriesView.as_view()),
    # 图片管理
    url(r'^skus/simple/$', skus.SKUSimpleView.as_view()),

    url(r'^goods/simple/$', spus.SPUSimpleView.as_view()),

    url(r'^goods/(?P<pk>\d+)/specs/$', spus.SPUSpecView.as_view()),

    url(r'^goods/brands/simple/$', spus.SPUViewSet.as_view({
        'get': 'simple',
    })),
    # POST /meiduo_admin/goods/images/
    url(r'^goods/images/$', spus.SPUViewSet.as_view({
        'post': 'image'
    })),

    url(r'^goods/channel/categories/$', spus.SPUCategoriesView.as_view()),

    url(r'^goods/channel/categories/(?P<pk>\d+)/$', spus.SPUTwoView.as_view()),

    url(r'^permission/content_types/$', permissions.PermissionViewSet.as_view({
        'get': 'content_types'
    })),

    url(r'^permission/simple/$', permissions.PermissionGroupsViewSet.as_view({
        'get': 'simple'
    })),

    url(r'^permission/groups/simple/$', permissions.PerssionsAdminViewSet.as_view({
        'get': 'simple'
    })),
    url(r'^goods/specs/simple/$', specs.SpecsOptionsViewSet.as_view({
        'get': 'simple'
    })),

]

# 商品频道信息
router = DefaultRouter()
router.register(r'goods/channels', channels.ChannelViewSet, base_name='channels')

router.register(r'skus/images', skus.SKUImageViewSet, base_name='images')

router.register('skus', skus.SKUViewSet, base_name='skus')

router.register('goods', spus.SPUViewSet, base_name='spus')

router.register('orders', orders.OrdersViewSet, base_name='orders')

router.register('permission/perms', permissions.PermissionViewSet, base_name='perms')

router.register('permission/groups', permissions.PermissionGroupsViewSet, base_name='groups')

router.register('permission/admins', permissions.PerssionsAdminViewSet, base_name='admins')

router.register('goods/specs', specs.SpecsViewSet, base_name='specs')

router.register('specs/options', specs.SpecsOptionsViewSet, base_name='specs')

router.register('goods/brands', brands.BrandsViewSet, base_name='specs')

urlpatterns += router.urls
