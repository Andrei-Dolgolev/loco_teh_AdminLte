from django.urls import path
from . import views


urlpatterns = [
    path('', views.profit_by_year, name='select-data'),
    path('all', views.profit_by_year_all, name='all'),
]