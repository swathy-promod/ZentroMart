from django.urls import path
from User import views
app_name="User"

urlpatterns = [
   path('Homepage/',views.Homepage,name="Homepage"),
   path('Myprofile/',views.myprofile,name="myprofile"),
   path('Editprofile/',views.editprofile,name="editprofile"),
   path('Changepassword/',views.changepassword,name="changepassword"),
   path('Complaint/',views.complaint,name="complaint"),
   path('Feedback/',views.feedback,name="feedback"),
   path('viewproduct/',views.viewproduct,name="viewproduct"),
   path('viewmore/<int:pid>',views.viewmore,name="viewmore"),
   path('viewcart/<int:id>',views.viewcart,name="viewcart"),
   path('addtocart/<int:pid>',views.addtocart,name="addtocart"),
   path('Mycart/',views.mycart,name="Mycart"),
   path("DelCart/<int:did>", views.DelCart,name="delcart"),
   path("CartQty/", views.CartQty,name="cartqty"),
   path('mybooking/',views.mybooking,name="mybooking"),
   path('payment/<int:id>',views.payment,name="payment"),
   path('rating/<int:mid>',views.rating,name="rating"),  
   path('viewrating/<int:mid>',views.viewrating,name="viewrating"),  
   path('ajaxstar/',views.ajaxstar,name="ajaxstar"),
   path('starrating/',views.starrating,name="starrating"),
   path('logout/',views.logout,name="logout"),

]