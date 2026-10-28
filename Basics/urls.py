from django.urls import path
from Basics import views

urlpatterns = [
   path('Sum/',views.Sum,name="Sum"),
   path('Sum2/',views.Sum2,name="Sum2"),
   path('Calculator/',views.Calculator,name="Calculator"),
   path('Largest/',views.Largest,name="Largest"),
   path('Largest3/',views.Largest3,name="Largest3"),
   path('RankList/',views.RankList,name="Ranklist"),
   path('BasicSalaryCalculations/',views.BasicSalaryCalculations,name="BasicSalaryCalculations"),
]

