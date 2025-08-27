from django.urls import path
from .views import CreateGame, GameView, HomeView, GameStateView

urlpatterns = [
    path("<int:pk>/", GameView.as_view(), name="game"),
    path("create/", CreateGame.as_view(), name="create_game"),
    path("<int:pk>/state/", GameStateView.as_view(), name="game_state"),
    path("", HomeView.as_view(), name="home"),
]
