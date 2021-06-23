from django.conf.urls import url
from user.views import login_auto,login_check
app_name = 'user'

urlpatterns = [
    url(r'^login_check$', login_check, name='login_check'), # 登录校验
    url(r'^login$', login_auto, name='login'), # 登录

]
