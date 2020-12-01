from game.models import Game


def current_game(request):
    game_id = request.session.get('game', 0)
    context = {}

    try:
        context['current_game'] = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        pass

    return context
