from django.urls import path
from Seller import views
from . import views
app_name="Seller"

urlpatterns = [
   path('Changepassword/',views.changepassword,name="changepassword"),
   path('myprofile/',views.myprofile,name="myprofile"), 
   path('Homepage/',views.Homepage,name="Homepage"),
   path('Editprofile/',views.editprofile,name="editprofile"),
   path('Product/',views.product,name="product"),
   path('ajaxsubcategory/',views.ajaxsubcategory,name="ajaxsubcategory"),
   path('productdelete/<int:id>/',views.productdelete, name="productdelete"),
   path('editproduct/<int:id>',views.editproduct,name="productedit"),
   path('addgallery/<int:id>',views.addgallery,name="addgallery"),
   path('Addstock/<int:id>',views.addstock,name="addstock"),
   path('viewbooking/',views.viewbooking,name='viewbooking'),
   path('orderpacked/<int:id>/', views.order_packed, name='orderpacked'),
   path('ordershipped/<int:id>/', views.order_shipped, name='ordershipped'),
   path('sales_dashboard/',views.shop_sales_dashboard,name="sales_dashboard"),
   path('logout/',views.logout,name="logout"),
]