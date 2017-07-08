
def is_user_login(request):
    ''' 判断用户是否登录 '''
    return request.user.is_authenticated()

