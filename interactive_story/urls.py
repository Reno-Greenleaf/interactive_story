"""interactive_story URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from interactive_story.views import Placeholder
from hub.views import Main, List, Authenticate, Logout, Register

urlpatterns = [
    path('admin/', admin.site.urls),
    # Hub
    path('', Main.as_view(), name='start'),
    path('stories', List.as_view(), name='list-stories'),
    path('create', Placeholder.as_view(), name='create-story'),
    path('edit', Placeholder.as_view(), name='list-own-stories'),
    path('login', Authenticate.as_view(), name='authenticate'),
    path('logout', Logout.as_view(), name='logout'),
    path('register', Register.as_view(), name='register'),
    path('play/<int:game_id>', Placeholder.as_view(), name='play'),
]
