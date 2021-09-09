from django.urls import path
from . import views

app_name='usuarios_app'
urlpatterns=[
    path('register/', views.Userregisterview.as_view(),name='registro'),
    path('login/', views.Loginuser.as_view(), name='loginuser'),
    path('logout/', views.Logoutview.as_view(), name='logoutuser'),
    path('update/', views.Updatepass.as_view(), name='update'),
    path('userver/<pk>/', views.Codeverify.as_view(), name='userverify'),
    path('panel/',)
]