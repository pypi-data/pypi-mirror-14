from score.http import RouterConfiguration


router = RouterConfiguration()


@router.route('home', '')
def home(ctx):
    raise Exception()
    return 'Hi there!'


def handle_404(ctx, error):
    pass


# @home.precondition
# def home_pre(ctx):
#     return 'x' in ctx.http.request.GET


# @router.route('greeeter', '{name}')
# def greeeter(ctx, name):
#     return 'Hi %s!' % name
