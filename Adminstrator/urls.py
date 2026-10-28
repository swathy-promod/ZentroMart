from django.urls import path
from Adminstrator import views
app_name="Admin"

urlpatterns = [
   path('AdminRegistration/',views.adminregistration,name="AdminRegistration"),
   path('District/',views.District,name="District"),
   path('Place/',views.place,name="Place"),
   path('Category/',views.Category,name="Category"),
   path('SubCategory/',views.subcategory,name="SubCategory"),
   path('districtdelete/<int:id>/',views.deletedistrict,name="districtdelete"),
   path('categorydelete/<int:id>/',views.deletecategory,name="deletecategory"),
   path('adminregistrationdelete/<int:id>/',views.deleteadminregistration,name="deleteadminregistration"),
   path('placedelete/<int:id>/',views.deleteplace,name="placedelete"),
   path('SubCategorydelete/<int:id>/',views.deletesubcategory,name="subcategorydelete"),
   path('editdistrict/<int:id>/',views.editdistrict,name="districtedit"),
   path('editcategory/<int:id>/',views.editcategory,name="categoryedit"),
   path('adminregistrationedit/<int:id>/',views.editadminregistration,name="adminregistrationedit"),
   path('editplace/<int:id>/',views.editplace,name="placeedit"),
   path('editsubcategory/<int:id>/',views.editsubcategory,name="subcategoryedit"),
   path('UserList/',views.userlist,name="userlist"),
   path('Homepage',views.homepage,name="Homepage"),
   path('acceptuser/<int:uid>/',views.useraccept,name="acceptuser"),
   path('rejectuser/<int:uid>/',views.userreject,name="rejectuser"),
   path('Reply/<int:id>/',views.reply,name="reply"),
   path('viewcomplaint/',views.viewcomplaint,name="viewcomplaint"),
   path('viewfeedback/',views.viewfeedback,name="viewfeedback"),
   path('sellerlist/',views.sellerlist,name="sellerlist"),
   path('acceptseller/<int:sid>/',views.selleraccept,name="acceptseller"),
   path('rejectseller/<int:sid>/',views.sellerreject,name="rejectseller"),
   path('dboylist/',views.dboylist,name="dboylist"),
   path('acceptdboy/<int:bid>/',views.dboyaccept,name="acceptdboy"),
   path('rejectdboy/<int:bid>/',views.dboyreject,name="rejectdboy"),
   path('Brand/',views.brand,name="Brand"),
   path('branddelete/<int:id>/',views.deletebrand,name="branddelete"),
   path('editbrand/<int:id>/',views.editbrand,name="brandedit"),
   path('logout/',views.logout,name="logout"),
   
]


