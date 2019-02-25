from django.conf.urls import url
from .import views

urlpatterns = [
    # 匹配首页
    url(r"^$", views.index),
    # 匹配login/
    url(r"^login/$", views.login),
    # 匹配register/
    url(r"^register/$", views.register),
    # 匹配cart/
    url(r"^cart/$", views.cart),
    # 使用post异步实现用户名验证
    url(r"^register-post/$", views.register_post),
    # 匹配　check_login/
    url(r"^check_login/$", views.check_login),
    # 匹配　type_goods/
    url(r"^type_goods", views.type_goods)
]