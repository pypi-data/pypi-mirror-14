from colab.plugins.utils.models import Collaboration
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import ast


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


def get_prefix():
    return settings.COLAB_APPS['colab_noosfero']['urls']['prefix'][1:-1]


class NoosferoCategory(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u"{}-{}".format(self.id, self.name)


class NoosferoSoftwareAdmin(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Noosfero Admin')
        verbose_name_plural = _('Noosfero Admins')


class NoosferoCommunity(Collaboration):

    id = models.IntegerField(primary_key=True)
    type = u'community'
    icon_name = u'file'
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(NoosferoCategory)
    admins = models.ManyToManyField(NoosferoSoftwareAdmin)
    created_at = models.DateTimeField(blank=True)
    thumb_url = models.CharField(max_length=255, null=True, blank=True)

    @property
    def url(self):
        return '/{prefix}/profile/{id}'.format(prefix=get_prefix(),
                                               id=self.identifier)

    @property
    def modified(self):
        return self.created_at

    def __unicode__(self):
        return u"{}({}) - {}".format(self.name, self.identifier,
                                     self.description)

    class Meta:
        verbose_name = _('Community')
        verbose_name_plural = _('Communities')


class NoosferoArticle(Collaboration):

    id = models.IntegerField(primary_key=True)
    type = u'articles'
    icon_name = u'file'
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True)
    path = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(NoosferoCategory)
    profile_identifier = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True)

    @property
    def url(self):
        return u'/{prefix}/{profile}/{path}'.format(
            prefix=get_prefix(),
            profile=self.profile_identifier,
            path=self.path
        )

    @property
    def modified(self):
        return self.created_at

    def __unicode__(self):
        return u"{}({})".format(self.title, self.path)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


class NoosferoSoftwareCommunity(models.Model):
    id = models.IntegerField(primary_key=True)
    type = u'software_community'
    icon_name = u'display'
    finality = models.CharField(max_length=255)
    repository_link = models.CharField(max_length=255, null=True)
    features = models.TextField(null=True)
    license_info = models.CharField(max_length=255)
    software_languages = ListField()
    software_databases = ListField()
    operating_system_names = ListField()
    community = models.ForeignKey('NoosferoCommunity')

    class Meta:
        verbose_name = _("Software Community")
        verbose_name_plural = _("Software Communities")
