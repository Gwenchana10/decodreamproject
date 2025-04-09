"""
URL configuration for interior_design project.

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
from designs.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_page, name="home_page"),
    path("home_page/", home_page, name="home_page"),
    path("front_page/", front_page, name="front_page"),
    path("promte_page/", promte_page, name="promte_page"),
    path('generate_design/', generate_design, name='generate_design'),
    path('image_style_page/', image_style_page, name='image_style_page'),
    path('generate_design1/', generate_design1, name='generate_design1'),
    path('chatbot_page/', chatbot_page, name='chatbot_page'),
    path('chatbot_api/', chatbot_api, name='chatbot_api'),
    path('login_page/', login_page, name='login_page'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('walktrough_page/', walktrough_page, name='walktrough_page'),
    path('walktrough_page2/', walktrough_page2, name='walktrough_page2'),
    path('interior_nav/', interior_nav, name='interior_nav'),
    path('user_designs/', user_designs, name='user_designs'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)