"""
URL configuration for noticeboard_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from noticeboard import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', views.register, name='register'),
    path('registration-confirmation/', views.registration_confirmation, name='registration_confirmation'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('view-advert/<int:advert_id>/', views.view_advert, name='view_advert'),
    path('create-edit-advert/', views.create_edit_advert, name='create_edit_advert'),
    path('create-edit-advert/<int:advert_id>/', views.create_edit_advert, name='edit_advert'),
    path('delete-advert/<int:advert_id>/', views.delete_advert, name='delete_advert'),
    path('view-responses/<int:advert_id>/', views.view_responses, name='view_responses'),
    path('leave-response/<int:advert_id>/', views.leave_response, name='leave_response'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('user-responses/', views.user_responses, name='user_responses'),
    path('my-responses/', views.my_responses, name='my_responses'),
    path('delete-response/<int:response_id>/', views.delete_response, name='delete_response'),
    path('accept-response/<int:response_id>/', views.accept_response, name='accept_response'),
    path('', views.home, name='home'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)