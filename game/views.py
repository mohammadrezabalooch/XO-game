from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.views.generic.detail import SingleObjectMixin
from .models import Game
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import random


# Create your views here.
def check_status(board, game):
    if (
        (board[0] == board[4] == board[8] == "X")
        or (board[2] == board[4] == board[6] == "X")
        or (board[0] == board[1] == board[2] == "X")
        or (board[0] == board[3] == board[6] == "X")
        or (board[2] == board[5] == board[8] == "X")
        or (board[6] == board[7] == board[8] == "X")
        or (board[3] == board[4] == board[5] == "X")
        or (board[1] == board[4] == board[7] == "X")
    ):
        if game.player1_symbol == "X":
            game.status = "w1"
            game.save()

            winner_player = game.player1
            loser_player = game.player2

        else:
            game.status = "w2"
            game.save()

            winner_player = game.player2
            loser_player = game.player1

        winner_player.wins += 1
        winner_player.save()
        loser_player.loses += 1
        loser_player.save()
    elif (
        (board[0] == board[4] == board[8] == "O")
        or (board[2] == board[4] == board[6] == "O")
        or (board[0] == board[1] == board[2] == "O")
        or (board[0] == board[3] == board[6] == "O")
        or (board[2] == board[5] == board[8] == "O")
        or (board[6] == board[7] == board[8] == "O")
        or (board[3] == board[4] == board[5] == "O")
        or (board[1] == board[4] == board[7] == "O")
    ):
        if game.player1_symbol == "O":
            game.status = "w1"
            game.save()

            winner_player = game.player1
            loser_player = game.player2

        else:
            game.status = "w2"
            game.save()

            winner_player = game.player2
            loser_player = game.player1

        winner_player.wins += 1
        winner_player.save()
        loser_player.loses += 1
        loser_player.save()
    elif " " not in board:
        game.status = "d"
        game.save()

        draw_player1 = game.player1
        draw_player1.draws += 1
        draw_player1.save()

        draw_player2 = game.player2
        draw_player2.draws += 1
        draw_player2.save()


class CreateGame(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        p1_symbol = random.choice(["X", "O"])
        p2_symbol = "O" if p1_symbol == "X" else "X"
        new_game = Game.objects.create(
            player1=request.user,
            player1_symbol=p1_symbol,
            player2_symbol=p2_symbol,
        )

        return redirect(new_game.get_absolute_url())


class GameView(LoginRequiredMixin, UserPassesTestMixin, SingleObjectMixin, View):
    model = Game

    def post(self, request, *args, **kwargs):
        current_game = self.get_object()
        if current_game.status == "p":
            pos = request.POST.get("position")
            if pos:
                position = int(pos)
                current_board = list(current_game.board)

                # conditions
                # for p1
                is_player1 = request.user == current_game.player1
                is_player1_turn = current_game.turn == current_game.player1_symbol
                # for p2
                is_player2 = request.user == current_game.player2
                is_player2_turn = current_game.turn == current_game.player2_symbol
                # both
                is_choose_empty = current_board[position] == " "

                if is_player1:
                    if is_player1_turn:
                        if is_choose_empty:
                            current_board[position] = current_game.player1_symbol
                            current_game.turn = current_game.player2_symbol
                            current_game.board = "".join(current_board)
                            current_game.save()
                            check_status(current_game.board, current_game)
                        else:
                            print("این خونه قبلا انتخاب شده")
                    else:
                        print("نوبت شما نیست")

                elif is_player2:
                    if is_player2_turn:
                        if is_choose_empty:
                            current_board[position] = current_game.player2_symbol
                            current_game.turn = current_game.player1_symbol
                            current_game.board = "".join(current_board)
                            current_game.save()
                            check_status(current_game.board, current_game)
                        else:
                            print("این خونه قبلا انتخاب شده")
                    else:
                        print("نوبت شما نیست")

                else:
                    return redirect("home")

            return redirect("game", pk=current_game.pk)
        else:
            print("بازی به اتمام رسیده")
            return redirect("game", pk=current_game.pk)

    def get(self, request, *args, **kwargs):
        current_game = self.get_object()

        if not current_game.player2 and request.user != current_game.player1:
            current_game.player2 = request.user
            current_game.save()

        context = {
            "game": current_game,
        }

        return render(request, "game/game.html", context)

    def test_func(self):
        current_game = self.get_object()
        if current_game.player1 and current_game.player2:
            return self.request.user in [current_game.player1, current_game.player2]
        return True


class HomeView(TemplateView):
    template_name = "game/home.html"
