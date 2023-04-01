from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
        path('login/',views.login,name='login'),
        path('logout/',views.logout,name='logout'),
        path('signup/',views.signup,name='signup'),
        path("send_otp/",views.send_otp,name="send_otp"),
]