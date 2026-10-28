from django.urls import path,include
from Guest import views
app_name="Guest"

urlpatterns = [
   path('User/',views.User,name="User"),
   path('ajaxplace/',views.ajaxplace,name="ajaxplace"),
   path('login/',views.login,name="login"),
   path('shop/',views.shopreg,name="shopreg"),
   path('dboy/',views.dboy,name="dboy"),
   
   path('',views.index,name='index'),
    path('forgotpassword/',views.forgotpassword,name="forgotpassword"),
    path('otp/',views.otp,name="otp"),
    path('newpass/',views.newpass,name="newpass"),


]


