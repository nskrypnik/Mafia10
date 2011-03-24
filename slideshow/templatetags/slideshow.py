from django import template
from django.conf import settings

register = template.Library()

def slideshow():
  """ Slideshow tag implementation """
  slide_image = 'slide-image'
  slide_list = []
  for i in range(1, 6):
    slide_list.append('slide-image-%i.jpg' % i) 
  return {'slide_list': slide_list, 'MEDIA_URL': settings.MEDIA_URL}

register.inclusion_tag('slideshow/slideshow.html')(slideshow)
