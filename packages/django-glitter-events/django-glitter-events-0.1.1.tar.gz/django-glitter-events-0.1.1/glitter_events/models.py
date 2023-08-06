# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse

from glitter.assets.fields import AssetForeignKey
from glitter.mixins import GlitterMixin
from glitter.models import BaseBlock


@python_2_unicode_compatible
class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('glitter-events:category-event-list', kwargs={
            'slug': self.slug,
        })


@python_2_unicode_compatible
class Event(GlitterMixin):
    category = models.ForeignKey('glitter_events.Category')
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique_for_date='start')
    location = models.CharField(max_length=128, blank=True)
    image = AssetForeignKey('glitter_assets.Image', null=True, blank=True)
    summary = models.TextField(help_text='A short sentence description of the event.')
    start = models.DateTimeField(help_text='Start time/date.')
    end = models.DateTimeField(help_text='End time/date.')
    date_url = models.DateField(db_index=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(GlitterMixin.Meta):
        ordering = ('start',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.date_url = self.start.date()
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('glitter-events:detail', kwargs={
            'year': self.date_url.year,
            'month': str(self.date_url.month).zfill(2),
            'day': str(self.date_url.day).zfill(2),
            'slug': self.slug,
        })


class UpcomingEventsBlock(BaseBlock):
    category = models.ForeignKey('glitter_events.Category', null=True, blank=True)

    class Meta:
        verbose_name = 'upcoming events'
