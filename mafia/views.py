# Create your views here.
from django.http import QueryDict, HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from lib import vkontakte
from middleware import VK_user

def login(request):
  """ Login to site with vkontakte api """
  next = request.REQUEST['next']
  vk_user_id = request.REQUEST['mid']
  # Check if the user id in request match the user id in cookies
  # If not, it's a deal of evil hackers. Fuck off them
  vk_cookie = request.COOKIES.get('vk_app_%s' % settings.VKONTAKTE_APP_ID)
  if vk_cookie:
    vk_cookie_set = QueryDict(vk_cookie)
    cookies_mid = vk_cookie_set.get('mid')
    if cookies_mid != vk_user_id:
      return fuckoff_hacker()
  else:
    return fuckoff_hacker()
  #TODO: authorization with session
  vk = vkontakte.API(settings.VKONTAKTE_APP_ID, settings.VKONTAKTE_SECRET_KEY)
  vk_profile = vk.getProfiles(uids=vk_user_id, fields='uid, photo, photo_medium, first_name, last_name, nickname')
  vk_user = VK_user(vk_profile[0])
  request.session['vk_user'] = vk_user
  return redirect(next)

def logout(request):
  request.session['vk_user'] = None
  next = request.REQUEST.get('next')
  if not next: next = '/'
  return redirect(next) 
  
def fuckoff_hacker():
  return HttpResponse('<h1>Fuck off dumb hacker!</h1>')
  