from models import Profile

class VK_user(object):
  """ Vkontakte user """
  
  def __init__(self, profile):
    self.uid = profile['uid']
    self.photo = profile['photo']
    self.photo_medium = profile['photo_medium']
    self.first_name = profile['first_name']
    self.last_name = profile['last_name']
    self.nickname = profile['nickname']
  
  def get_profile(self):
      try:
          profile = Profile.objects.get(vkontakte_id = self.uid, is_active=True)
      except Profile.DoesNotExist:
          return None
      return profile
class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Mafia authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        request.__class__.vk_user = request.session.get('vk_user')
        return None