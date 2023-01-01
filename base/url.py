from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('',views.home,name = 'home'),
    path('tiepnhanhs/', views.TiepnhanHS, name = 'TiepnhanHS'),
    path('search-student', views.searchStudent, name='search'),
    path('receive-transcripts', views.receiveTranscripts, name='transcripts'),
    path("quanlidotuoi/", views.quanlidotuoi, name='quanlidotuoi'),
    path("quanlidotuoi/capnhat/<int:age_id>", views.capNhatTuoi, name='capNhatTuoi'),
    path("quanlidotuoi/delete/<int:age_id>", views.xoaTuoi, name='xoaTuoi'),
    path("age/add", views.themTuoi, name='themTuoi'),
    path("nienkhoa/", views.nienkhoa, name='nienkhoa'),
    path("lapdanhsachlop/<int:age_id>", views.lapDSlop, name='lapDSlop')
    
]
