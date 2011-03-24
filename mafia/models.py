# -*- coding: utf-8 -*-
from django.db import models

class Location(models.Model):
  lng = models.IntegerField(blank = True)
  lat = models.IntegerField(blank = True)
  name = models.CharField(max_length=526, blank=False, verbose_name="Название места")
  address = models.CharField(max_length = 526, blank=False)  
  
  class Meta:
    verbose_name = "Место проведения" 
    verbose_name_plural = "Места проведения"
    
class Tournament(models.Model):
  name = models.CharField(max_length = 526, blank=False, verbose_name="Название турнира")
  desc = models.TextField() 
  
  class Meta:
    verbose_name = "Турнир"
    verbose_name_plural = "Турниры"    

class Game(models.Model):
  begin_time = models.DateTimeField(verbose_name = "Начало")
  end_time = models.DateTimeField(verbose_name = "Окончание", blank = True) 
  location = models.ForeignKey(Location, null=False)
  tables = models.IntegerField(default = 1, verbose_name = "Количество столов")
  tournament = models.ForeignKey(Tournament, null=True, blank=True) 
  
  class Meta:
    verbose_name = "Игра"
    verbose_name_plural = "Игры"    