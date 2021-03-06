from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import password_reset, password_reset_done

urlpatterns = [
    url(r'^$',views.home, name='home'),
    url(r'^login/$',views.login_user, name='login'),
    url(r'^signup/$',views.signup, name='signup'),
    url(r'^appointment/$',views.appointment, name='appointment'),
    url(r'^forgetpassword/$',views.forgetpassword, name='forgetpassword'),
]