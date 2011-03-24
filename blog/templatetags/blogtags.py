from django.template.defaultfilters import stringfilter
from django import template
from django.utils.safestring import mark_safe
from blog.models import Entry
from tagging.models import Tag
from tagging import utils as tagutils

MIN_FONT_SIZE = 11

register = template.Library()

@register.filter(name='blogtags')
def blogtags(entry_tags):
    retval = ''
    for tag in entry_tags:
        a_href = '<a href="/blog/bytag/%s">' % tag.name
        a_close = '</a>'
        retval += a_href + tag.name + a_close
        if tag != entry_tags[len(entry_tags) - 1]:
            retval += ", "
    return mark_safe(retval)

@register.filter(name='true_font_size')
def true_font_size(value):
    return MIN_FONT_SIZE + 2*value

@register.inclusion_tag('last_posts.html')
def lastposts(username):
    if username == "admin":
        entry_list = Entry.objects.all()[:3]
    else:
        entry_list = Entry.objects.filter(status=Entry.LIVE_STATUS)[:3]
    return { 'entry_list': entry_list }

@register.inclusion_tag('blog_cloud.html')
def blogcloud():
    tags = Tag.objects.usage_for_model(Entry, counts=True)
    tags = tagutils.calculate_cloud(tags)
    return {'tags': tags}