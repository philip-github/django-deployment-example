from django.urls import re_path
from login_app import views

app_name = 'login_app'

urlpatterns = [
    re_path(r'^regitser/$',views.regitser,name='regitser'),
    re_path(r'^user_login/$',views.user_login,name='user_login'),
]
