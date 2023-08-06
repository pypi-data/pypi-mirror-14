import json
import urllib
import urllib2
import logging

from dateutil.parser import parse

from django.db.models.fields import DateTimeField

from colab.plugins.data import PluginDataImporter

from colab.plugins.models import TimeStampPlugin
from colab_noosfero.models import (NoosferoArticle, NoosferoCommunity,
                                   NoosferoCategory, NoosferoSoftwareCommunity,
                                   NoosferoSoftwareAdmin)

LOGGER = logging.getLogger('colab_noosfero')


class NoosferoDataImporter(PluginDataImporter):
    app_label = 'colab_noosfero'

    def get_request_url(self, path, **kwargs):
        upstream = self.config.get('upstream')
        kwargs['private_token'] = self.config.get('private_token')

        params = urllib.urlencode(kwargs)

        if upstream[-1] == '/':
            upstream = upstream[:-1]

        return u'{}{}?{}'.format(upstream, path, params)

    def get_json_data(self, api_url, page, per_page=250, **kwargs):
        url = self.get_request_url(api_url, per_page=per_page, page=page,
                                   **kwargs)

        try:
            data = urllib2.urlopen(url, timeout=1000)
            json_data = json.load(data)
        except urllib2.URLError:
            LOGGER.exception("Connection timeout: " + url)
            json_data = {}

        return json_data

    def fill_object_data(self, element, _object):
        for field in _object._meta.fields:
            try:
                if field.name == "user":
                    _object.update_user(
                        element["author"]["name"])
                    continue

                if field.name == "username":
                    _object.username = element["author"]["identifier"]

                if field.name == "profile_identifier":
                    _object.profile_identifier = \
                        element["profile"]["identifier"]
                    continue

                if field.name == "license_info":
                    _object.license_info = element["license_info"]["version"]
                    continue

                if field.name == "software_languages":
                    _object.software_languages = element["software_languages"]
                    continue

                if field.name == "software_databases":
                    _object.software_databases = element["software_databases"]
                    continue

                if field.name == "operating_system_names":
                    _object.operating_system_names = element[
                        "operating_system_names"]
                    continue

                if field.name == "community":
                    _object.community_id = element["community_id"]
                    continue

                if isinstance(field, DateTimeField):
                    value = parse(element[field.name])
                else:
                    value = element[field.name]

                setattr(_object, field.name, value)
            except KeyError:
                continue
            except TypeError:
                continue
            except:
                continue

        return _object

    def fetch_communities(self):
        url = '/api/v1/communities'
        timestamp = TimeStampPlugin.get_last_updated('NoosferoCommunity')

        page = 1
        can_updated_timestamp = True
        while True:
            json_data = self.get_json_data(url, page, timestamp=timestamp,
                                           order="updated_at DESC")

            if not len(json_data) or not len(json_data.get('communities', [])):
                break

            json_data = json_data['communities']
            if can_updated_timestamp:
                self.save_last_update(json_data[0]['updated_at'],
                                      'NoosferoCommunity')
                can_updated_timestamp = False

            for element in json_data:
                community = NoosferoCommunity()
                self.fill_object_data(element, community)

                if element['image']:
                    community.thumb_url = element['image']['thumb_url']

                try:
                    community.save()
                except:
                    continue

                if 'categories' in element:
                    self.fetch_community_categories(community,
                                                    element["categories"])

                if 'admins' in element:
                    self.fetch_software_admins(community, element["admins"])
            page += 1

    def fetch_community_categories(self, community, json_data):
        for element in json_data:
            category = NoosferoCategory.objects.get_or_create(
                id=element["id"], name=element["name"])[0]
            community.categories.add(category.id)

    def fetch_software_admins(self, community, json_data):
        for element in json_data:
            software_admin = NoosferoSoftwareAdmin.objects.get_or_create(
                id=element["id"], name=element["name"],
                username=element["username"])[0]
            community.admins.add(software_admin.id)

    def fetch_software_communities(self):
        url = '/api/v1/software_communities'
        timestamp = TimeStampPlugin.get_last_updated(
            'NoosferoSoftwareCommunity')

        can_updated_timestamp = True
        page = 1
        while True:
            json_data = self.get_json_data(url, page, timestamp=timestamp,
                                           order="updated_at DESC")

            if not len(json_data) or not len(json_data.get('software_infos',
                                             [])):
                break

            json_data = json_data['software_infos']
            if can_updated_timestamp:
                self.save_last_update(json_data[0]['updated_at'],
                                      'NoosferoSoftwareCommunity')
                can_updated_timestamp = False

            for element in json_data:
                software_community = NoosferoSoftwareCommunity()
                self.fill_object_data(element, software_community)

                try:
                    software_community.save()
                except:
                    continue
            page += 1

    def fetch_articles(self):
        url = '/api/v1/articles'
        timestamp = TimeStampPlugin.get_last_updated('NoosferoArticle')

        can_updated_timestamp = True
        page = 1
        while True:
            json_data = self.get_json_data(url, page, timestamp=timestamp,
                                           order="updated_at DESC")

            if not len(json_data) or not len(json_data.get('articles', [])):
                break

            json_data = json_data['articles']
            if can_updated_timestamp:
                self.save_last_update(json_data[0]['updated_at'],
                                      "NoosferoArticle")
                can_updated_timestamp = False

            for element in json_data:
                article = NoosferoArticle()
                self.fill_object_data(element, article)

                try:
                    article.save()
                except:
                    continue

                for category_json in element["categories"]:
                    category = NoosferoCategory.objects.get_or_create(
                        id=category_json["id"], name=category_json["name"])[0]
                    article.categories.add(category.id)
            page += 1

    def save_last_update(self, last_updated, class_name):
        TimeStampPlugin.update_timestamp(class_name, last_updated=last_updated)

    def fetch_data(self):
        LOGGER.info("Importing Communities")
        self.fetch_communities()

        LOGGER.info("Importing Articles")
        self.fetch_articles()

        LOGGER.info("Importing Software Communities")
        self.fetch_software_communities()
