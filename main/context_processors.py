from .models import Users

def current_user(request):
    user = None
    if 'user_uid' in request.session:
        try:
            user = Users.objects.get(uid=request.session['user_uid'])
        except Users.DoesNotExist:
            request.session.flush()
    return {'user': user}
