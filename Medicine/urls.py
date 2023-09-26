from django.urls import path
from . import views

urlpatterns = [
   
   path('', views.Signup,name= "signup"),
   path('login/',views.Login,name= 'login'),
   path('logout/',views.Logout,name= 'logout'),
   path('add/',views.Add,name= 'add'),
   path('list/',views.List,name ='list'),
   path('list/update/<int:id>',views.Update,name="update"),
   path('list/delete/<int:id>',views.Delete,name='delete'),
   path('search/',views.Search,name="search")  
   
]
