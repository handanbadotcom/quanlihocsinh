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
    path("lapdanhsachlop/<age_id>", views.lapDSlop, name='lapDSlop'),
    

    path('class_setting/', views.class_setting, name = 'class_setting'),
    path('class_setting/delete/<str:pk>', views.class_setting_delete, name='class_setting_delete'),
    path('class_setting/update/<str:pk>', views.class_setting_update, name='class_setting_update'),

    path('subject_setting/', views.subject_setting, name = 'subject_setting'),
    path('subject_setting/delete/<str:pk>', views.subject_setting_delete, name='subject_setting_delete'),
    path('subject_setting/update/<str:pk>', views.subject_setting_update, name='subject_setting_update'),
]

