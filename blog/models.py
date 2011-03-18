# coding: UTF-8
from django.db import models
import datetime
from django.contrib.auth.models import User
from tagging.fields import TagField
from markdown import markdown
 
class Category(models.Model):
	title = models.CharField(max_length=250, verbose_name=u'Название',
		help_text=u'Максимум 250 символов.')
	slug = models.SlugField(unique=True, verbose_name=u'Символьный идентификатор',
		help_text=u"Символьный идентификатор для формирования адреса категории. Может содержать латинские буквы, знак подчёркивания и дефис. Должен быть уникален.")
	description = models.TextField(verbose_name=u'Описание категории')
 
	class Meta:
		ordering = ['title']
		verbose_name = u"Категория"
		verbose_name_plural = u"Категории"
 
	def __unicode__(self):
		return self.title
 
	def get_absolute_url(self):
		return "/categories/%s/" % self.slug

class Entry(models.Model):
	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	HIDDEN_STATUS = 3
	STATUS_CHOICES = ((LIVE_STATUS, u'Опубликована'),
			  (DRAFT_STATUS, u'Черновик'),
			  (HIDDEN_STATUS, u'Скрытая'))
 
	# article core
	title = models.CharField(max_length=250,  verbose_name=u'Название', help_text=u'Максимум 250 символов.')
	excerpt = models.TextField(blank=True, verbose_name=u'Краткая выдержка из статьи', help_text=u'Поле можно оставить пустым.')
	body = models.TextField(verbose_name=u'Статья')
	pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'Дата публикации')
 
	# cached HTML
	excerpt_html = models.TextField(editable=False, blank=True)	# excerpt is Markdown, excerpt_html is HTML
	body_html = models.TextField(editable=False, blank=True)		# body is Markdown, body_html is HTML
 
	# some metadata
	slug = models.SlugField(unique_for_date='pub_date',
			verbose_name=u'Символьный идентификатор',
			help_text=u"Символьный идентификатор для формирования адреса статьи. Может содержать латинские буквы, знак подчёркивания и дефис. Должен быть уникален среди всех статей за этот день.")
	author = models.ForeignKey(User,  verbose_name=u'Автор')
	enable_comments = models.BooleanField(default=True,  verbose_name=u'Разрешить комментарии')
	featured = models.BooleanField(default=False,  verbose_name=u'Важная статья')
	status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS,  verbose_name=u'Статус')
 
	# categorization
	categories = models.ManyToManyField(Category,  verbose_name=u'Категории', blank=True)
	tags = TagField(verbose_name=u'Метки', help_text=u'Метки статьи, разделённые пробелами или запятыми.')
	# Blog image
	postimage = models.ImageField(upload_to = "blogimages", blank=True)
 
	class Meta:
		verbose_name = u"Статья"
		verbose_name_plural = u"Статьи"
		ordering = ['-pub_date']
 
	def __unicode__(self):
		return self.title
 
	def save(self):	# override models.Model.save()
		self.body_html = markdown(self.body)
		if self.excerpt:
			self.excerpt_html = markdown(self.excerpt) 
		super(Entry, self).save()
		
 
	def get_absolute_url(self):		# link "see on site" will be available in admin site
		return "/blog/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)
	
	def small_img_url(self):
		return self.postimage.__str__().replace('blogimages', 'blogimages/small')
	
	def thumb_img_url(self):
		return self.postimage.__str__().replace('blogimages', 'blogimages/thumb')
	

