from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils.text import slugify


class City(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def first_letter(self):
        return self.title and self.title.upper()[0] or ''

    def save(self, *args, **kwargs):
        for field_name in ['title']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        super(City, self).save(*args, **kwargs)


class Ad(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    city = models.ForeignKey(City)
    date = models.DateField(default=datetime.date.today)
    contact = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Ad'
        verbose_name_plural = 'Ads'

    def __unicode__(self):
        return self.title


def get_image_filename(instance, filename):
    title = instance.ad.title
    slug = slugify(title)
    return "ad_image/%s-%s" % (slug, filename)


class Images(models.Model):
    ad = models.ForeignKey(Ad, default=None)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image', null=True, blank=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
