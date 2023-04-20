from django.urls import path
from . import views

urlpatterns = [
    path('', views.acoesList, name='acao-list'),
    path('acao/<int:id>', views.acoesView, name="acao-view"),
    path('newacao/', views.newAcao, name="new-acao"),
    path('edit/<int:id>', views.editAcao, name="edit-acao"),
    path('delete/<int:id>', views.deleteAcao, name="delete-acao"),
]