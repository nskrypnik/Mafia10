from django.conf import settings

def vkontakte(request):
  return {'VKONTAKTE_APP_ID': settings.VKONTAKTE_APP_ID,
          'VKONTAKTE_SECRET_KEY': settings.VKONTAKTE_SECRET_KEY
          }
          
def auth(request):
  return {'vk_user': request.vk_user}