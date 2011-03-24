# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from blog.models import Entry
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from tagging.models import Tag
from tagging.models import TaggedItem
from django.core.paginator import Paginator
try:
	import Image
except ImportError:
	from PIL import Image
 
def entries_index(request):
	if request.user.username == "admin":
		raw_entry_list = Entry.objects.all()
	else:
		raw_entry_list = Entry.objects.filter(status=Entry.LIVE_STATUS)
	paginator = Paginator(raw_entry_list, 7)
	try:
		 page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
		
	try:
		entry_list = paginator.page(page)
	except (EmptyPage, InvalidPage):
		entry_list = paginator.page(paginator.num_pages)
	
	return render_to_response('entry_index.html', { 'entry_list': entry_list }, 
							  context_instance=RequestContext(request) )
 
def entry_detail(request, year, month, day, slug):
	import datetime, time
	date_stamp = time.strptime(year+month+day, "%Y%b%d")
	pub_date = datetime.date(*date_stamp[:3])
	entry = get_object_or_404(Entry, pub_date__year=pub_date.year,
		pub_date__month=pub_date.month, pub_date__day=pub_date.day,
		slug=slug)
	entry_tags = Tag.objects.get_for_object(entry)
	return render_to_response('entry_detail.html', { 'entry': entry, 'entry_tags': entry_tags },
							  context_instance=RequestContext(request) )

def entry_bytag(request, tag):
	#entry_list = Entry.objects.filter(tags__contains='\'' + tag + '\'')
	tag_inst = Tag.objects.get(name=tag)
	raw_entry_list = TaggedItem.objects.get_by_model(Entry, tag_inst)
	if request.user.username != "admin":
		raw_entry_list = raw_entry_list.filter(status=Entry.LIVE_STATUS)
	
	paginator = Paginator(raw_entry_list, 7)
	try:
		 page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
		
	try:
		entry_list = paginator.page(page)
	except (EmptyPage, InvalidPage):
		entry_list = paginator.page(paginator.num_pages)
		
	return render_to_response('entry_bytag.html', { 'entry_list': entry_list, 'tag': tag },
							  context_instance=RequestContext(request) )
	
def resize(request, width, height, path):
	# Кеширование
	cache_file = "tmp/cache/" + "%s_%s_%s" % (width, height, path.replace('/', '_'))
	try:
		image = Image.open(cache_file)
	except IOError:
		image = Image.open(settings.MEDIA_ROOT + '/%s' % (path))
		image.thumbnail((int(width), int(height)), Image.ANTIALIAS)
		image.save(cache_file, "PNG")
	response = HttpResponse(mimetype="image/jpg")
	image.save(response, "PNG")
	return response
