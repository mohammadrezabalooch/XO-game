from django.urls import path
from .views import CreateGame, GameView

url_patterns = [
    path("", GameView, name="game"),
    path("create/", CreateGame.as_view(), name="create_game"),
]
