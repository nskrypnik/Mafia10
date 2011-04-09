# -*- coding: utf-8 -*-
# Create your views here.
from django.http import QueryDict, HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from lib import vkontakte
from middleware import VK_user
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Profile
from django.core.validators import email_re
import re

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
    
def joinus(request):
    vkuser = request.session.get('vk_user')
    if vkuser:
        try:
            profile = Profile.objects.get(vkontakte_id = vkuser.uid)
            is_member = True
            is_active = profile.is_active
        except Profile.DoesNotExist:
            is_member = False
            is_active = False
    else:
        is_member = False
        is_active = False
    
    ec = {'vkuser': vkuser, 'is_member': is_member, 'is_active': is_active}
    return render_to_response('joinus.html', ec, context_instance=RequestContext(request))
    


def handle_join(request):
    # Handle request here
    vkuser = request.session.get('vk_user')
    errors = {}
    phone = request.REQUEST.get('phone')
    email = request.REQUEST.get('email')
    if phone:
        if not phone_validate(phone):
            errors["phone_error"] = u'Введите правильный телефон'
    else:
        errors['phone_error'] = u'Это поле не должно быть пустым'
        
    if email:
        if not email_validate(email):
            errors['email_error'] = u'Введите корректный e-mail'
    else:
        errors['email_error'] = u'Это поле не должно быть пустым'
    
    if errors:
        ec = {'vkuser': vkuser, 'email': email, 'phone': phone}
        ec.update(errors)
        return render_to_response('joinus.html', ec, context_instance=RequestContext(request))
    else:
        p = Profile(name = ' '.join([vkuser.first_name, vkuser.last_name]),
            vkontakte_id = vkuser.uid, email = email, phone = phone,
            photo = vkuser.photo, photo_medium = vkuser.photo_medium,
            status = u'Игрок')
        p.save()
        return redirect('/thankyou/')

def phone_validate(val):
    if re.match('^((0|\+38)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', val):
        return True
    return False

def email_validate(val):
    if email_re.match(val): return True
    return False

def members_list(request):
    members = Profile.objects.filter(is_active = True)
    return render_to_response('mafiosi.html', {'members': members}, context_instance=RequestContext(request))

def fuckoff_hacker():
    return HttpResponse('<h1>Fuck off dumb hacker!</h1>')
    