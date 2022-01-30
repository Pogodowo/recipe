from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home,name='home'),
    path('mojerec',views.mojeRec,name='mojerec'),
    path('dodajrec',views.dodajRec,name='dodajrec'),
    path('receptura/(<int:receptura_id>)',views.receptura,name='receptura'),
    path('formJson/<str:skl>/', views.formJson, name='formJson'),
    path('receptura/formJson/<str:skl>/', views.formJson, name='formJson'),
    #`receptura/dodajskl/${ sklId }/`
    path('receptura/dodajskl/<str:sklId>/', views.dodajsklJson, name='dodajsklJson'),
    #path('receptura/dodajskl', views.dodajsklJson, name='dodajsklJson'),`aktualizujTabela/${sklId}/`
    path('receptura/aktualizujTabela/<str:sklId>/', views.aktualizujTabela, name='aktualizujTabela'),
    path('receptura/delSkl/<int:id>/', views.delSkl, name='delSkl'),


]
