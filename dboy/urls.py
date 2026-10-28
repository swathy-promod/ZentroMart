from django.urls import path
from dboy import views
app_name="dboy"

urlpatterns = [ 
   path('Homepage/',views.homepage,name="Homepage"),
   path('myprofile/',views.myprofile,name="myprofile"),
   path('Changepassword/',views.changepassword,name="changepassword"), 
   path('Editprofile/',views.editprofile,name="editprofile"),
   path('viewbooking/',views.viewbooking,name='viewbooking'),
   path('Myorder/', views.MyOrder, name='Myorder'),
   path('order_collect/<int:id>/', views.order_collect, name='order_collect'),
   path('outfordelivery/<int:id>/', views.out_for_delivery, name='outfordelivery'),
   path('delivered/<int:id>/', views.delivered, name='delivered'),
    path('logout/',views.logout,name="logout"),
]