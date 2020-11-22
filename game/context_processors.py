from game.models import Game


def current_game(request):
    game_id = request.session.get('game', 0)

    if game_id:
        game = Game.objects.get(pk=game_id)
        return {'current_game': game}
    else:
        return {}
