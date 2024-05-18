from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.data, name='data'),
    path('form/<uuid:form_id>/', views.form, name='get_form_by_id'),
    path('create/', views.create, name='create'),
    path('create-answers/', views.create_answers, name='create_answers'),
]