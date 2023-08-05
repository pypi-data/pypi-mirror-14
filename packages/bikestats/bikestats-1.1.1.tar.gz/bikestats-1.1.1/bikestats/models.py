from __future__ import unicode_literals

import os
from bs4 import BeautifulSoup
from django.db import models, IntegrityError

from bikestats.scraper import Scraper


class Make(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name',)


class Model(models.Model):
    name = models.CharField(max_length=200)
    make = models.ForeignKey(Make)
    year_start = models.IntegerField(null=True, blank=True)
    year_end = models.IntegerField(null=True, blank=True)
    description = models.TextField(default='')
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        year_append = self.year-start + '-' if self.year-start else ''
        return self.make.name + ' ' + self.name + ' ' + year_append

    class Meta:
        unique_together = ('name', 'make', 'year_start', 'year_end')


class Stat(models.Model):
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=64)
    model = models.ForeignKey(Model)

    def __unicode__(self):
        return unicode(self.model) + "'s " + self.name

    class Meta:
        unique_together = ('name', 'model')


def parse_all(scraped_root_path):
    """ Parse all bike information and stick in database. Current naive-mode *shrugs*

    Args:
        scraped_root_path: Path to the scraped directory of the website
    """
    soup = BeautifulSoup(open(os.path.join(scraped_root_path, 'index.html')).read(), "html.parser")
    for name_make, make_href in Scraper.parse_makes(soup):
        make, created_make = Make.objects.get_or_create(name=name_make)
        make_soup = BeautifulSoup(open(os.path.join(scraped_root_path, make_href)).read(), "html.parser")
        models, description_make, pages = Scraper.parse_make(make_soup, name=name_make)
        for page in pages:
            path = os.path.join(scraped_root_path, 'bikes', page)
            try:
                page_soup = BeautifulSoup(open(path).read(), "html.parser")
                _models, _d, _p = Scraper.parse_make(page_soup, name=name_make)
                models.extend(_models)
            except:
                print 'Failed to parse page with path: ' + path
        for name_model, model_href, year_start, year_end in models:
            kwargs = {}
            if year_start:
                kwargs['year_start'] = year_start
                if year_end:
                    kwargs['year_end'] = year_end
            model, created_model = Model.objects.get_or_create(name=name_model, make=make, **kwargs)
            model_soup = BeautifulSoup(open(os.path.join(scraped_root_path, 'bikes', model_href)).read(), "html.parser")
            name_model_2, description_model, stats = Scraper.parse_model(model_soup, make_name=name_make, model_name=name_model)
            for name_stat, value in stats:
                try:
                    Stat.objects.update_or_create(name=name_stat, value=value, model=model)
                except IntegrityError:
                    print 'IntegrityError for make/model: ' + name_make + '/' + name_model + " stat: " + name_stat
