"""
URL configuration for gridiron project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from core import views as core_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/auth/signup/', core_views.SignUpView.as_view(), name='user-signup'),
    path('api/auth/signin/', core_views.SignInView.as_view(), name='user-signin'),
    path('api/auth/signout/', core_views.SignOutView.as_view(), name='user-signout'),
    path('api/auth/signout-all/', core_views.SignOutAllView.as_view(), name='signout-all'),
    path('api/auth/status/', core_views.AuthStatusView.as_view(), name='auth-status'),
    
    path('api/auth/', include('knox.urls')),
    
    path('api/core/', include('core.urls')),
    path('api/sleeper/', include('sleeper.urls')),
]
