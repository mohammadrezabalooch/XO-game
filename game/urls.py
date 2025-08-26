from django.urls import path
from .views import CreateGame, GameView, HomeView

urlpatterns = [
    path("<int:pk>/", GameView.as_view(), name="game"),
    path("create/", CreateGame.as_view(), name="create_game"),
    path("", HomeView.as_view(), name="home"),
]
