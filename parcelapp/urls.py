from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(),name='home'),
    path('success/<int:parcel>/', views.Success.as_view(), name='success'),
    path('searchparcel', views.ParcelArrival.as_view(), name='search'),
    path('searchparcel/results', views.ParcelResults.as_view(), name='results'),
    path('searchparcel/results/<int:pk>/', views.ParcelDetailView.as_view(),name='detailedresult'),
    path('searchparcel/results/<int:pk>/discharge', views.DischargeView.as_view(),name='discharge'),
    path('searchparcel/results/<int:pk>/alert', views.AlertView.as_view(),name='alert'),
]
