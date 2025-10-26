from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test_design, name='test_design'),
    path('search/', views.simple_search, name='simple_search'),
    path('advanced-search/', views.advanced_search, name='advanced_search'),
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('properties/add/', views.PropertyCreateView.as_view(), name='property_create'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('properties/<int:pk>/edit/', views.PropertyUpdateView.as_view(), name='property_update'),
    path('properties/<int:pk>/delete/', views.PropertyDeleteView.as_view(), name='property_delete'),
    path('properties/<int:property_id>/add-internet-photos/', views.add_internet_photos, name='add_internet_photos'),
    path('sale/', views.sale_properties, name='sale'),
    path('rent/', views.rent_properties, name='rent'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

