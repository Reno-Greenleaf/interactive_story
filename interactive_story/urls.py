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
from event.views import Events
from command.views import AddCommand, EditCommand, DeleteCommand
from game.views import CreateGame, DeleteGame, EditGame, SelectGame, Games
from place.views import AddPlace, EditPlace, DeletePlace
from player.views import Play, Start, Continue
from custom_user.views import Login, Logout
from conversation.views import AddExchange, EditExchange, DeleteExchange, Exchange
from hub.views import Main, List

urlpatterns = [
    # path('', Games.as_view(), name='games'),
    path('admin/', admin.site.urls),
    path('events', Events.as_view(), name='events'),
    path('command/add', AddCommand.as_view(), name='add-command'),
    path('command/edit/<int:command_id>', EditCommand.as_view(), name='edit-command'),
    path('command/delete/<int:command_id>', DeleteCommand.as_view(), name='delete-command'),
    path('game/edit', EditGame.as_view(), name='edit-game'),
    path('game/create', CreateGame.as_view(), name='create-game'),
    path('game/delete', DeleteGame.as_view(), name='delete-game'),
    path('game/select/<int:game_id>', SelectGame.as_view(), name='select-game'),
    path('place/add', AddPlace.as_view(), name='add-place'),
    path('place/edit/<int:place_id>', EditPlace.as_view(), name='edit-place'),
    path('place/delete/<int:place_id>', DeletePlace.as_view(), name='delete-place'),
    # path('play', Play.as_view(), name='play'),
    path('start/<int:game_id>', Start.as_view(), name='start'),
    path('continue/<int:session_id>', Continue.as_view(), name='continue'),
    # path('login', Login.as_view(), name='login'),
    # path('logout', Logout.as_view(), name='logout'),
    path('add-exchange', AddExchange.as_view(), name='add-exchange'),
    path('edit-exchange/<int:exchange_id>', EditExchange.as_view(), name='edit-exchange'),
    path('delete-exchange/<int:exchange_id>', DeleteExchange.as_view(), name='delete-exchange'),
    path('conversation/<int:exchange_id>', Placeholder.as_view(), name='exchange'),
    # Hub
    path('', Main.as_view(), name='start'),
    path('stories', List.as_view(), name='list-stories'),
    path('create', Placeholder.as_view(), name='create-story'),
    path('edit', Placeholder.as_view(), name='list-own-stories'),
    path('login', Placeholder.as_view(), name='authenticate'),
    path('logout', Placeholder.as_view(), name='logout'),
    path('play/<int:game_id>', Placeholder.as_view(), name='play'),
]
