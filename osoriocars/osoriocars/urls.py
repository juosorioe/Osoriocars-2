from django.contrib import admin
from django.urls import path
from authapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index_view, name='index'),  # Ensure this points to index_view
    path('servicios/', views.services_view, name='servicios'),
    path('contacto/', views.contact_view, name='contacto'),
    path('sobre/', views.about_view, name='sobre'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('toggle-mechanic/<int:user_id>/', views.toggle_mechanic_status, name='toggle_mechanic_status'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('add-to-cart/<int:service_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:service_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('manage-services/', views.manage_services, name='manage_services'),
    path('add-service/', views.add_service, name='add_service'),
    path('edit-service/<int:pk>/', views.edit_service, name='edit_service'),
    path('remove-service/<int:pk>/', views.remove_service, name='remove_service'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile_view, name='profile'),
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
