from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.


class Game(models.Model):
    GAME_STATUS_CHOICES = [
        ("p", "in progress"),
        ("w1", "p1 won"),
        ("w2", "p2 won"),
        ("d", "draw"),
    ]
    SYMBOL_CHOICES = [
        ("X", "X"),
        ("O", "O"),
    ]
    player1 = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="player1"
    )
    player2 = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="player2",
        null=True,
        blank=True,
    )
    turn = models.CharField(max_length=1, default="X")
    status = models.CharField(max_length=2, default="p", choices=GAME_STATUS_CHOICES)
    board = models.CharField(max_length=9, default="         ")
    player1_symbol = models.CharField(max_length=1, choices=SYMBOL_CHOICES, default="X")
    player2_symbol = models.CharField(max_length=1, choices=SYMBOL_CHOICES, default="O")

    def get_absolute_url(self):
        return reverse("game", kwargs={"pk": self.pk})


# class Move(models.Model):
#     Game = models.ForeignKey(Game, related_name="moves", on_delete=models.CASCADE)
#     player_symbol = models.CharField(max_length=1)
#     position = models.IntegerField()

#     class Meta:
#         unique_together = ("game", "position")
