from django.utils.translation import ugettext as _
from colab_noosfero.models import NoosferoCategory


def get_filters(request):
    return {
        'community': {
            'name': _(u'Communities'),
            'icon': 'globe',
            'fields': (
                ('title', _(u'Name'), request.get('title')),
                (
                    'description',
                    _(u'Description'),
                    request.get('description'),
                ),
                (
                    'category', _(u'Category'), request.get('category'),
                    'list',
                    [(v, v) for v in NoosferoCategory.objects.values_list(
                     'name', flat=True)]
                ),
            ),
        },
        'articles': {
            'name': _(u'Article'),
            'icon': 'list-alt',
            'fields': (
                ('title', _(u'Title'), request.get('title')),
                (
                    'body',
                    _(u'Content'),
                    request.get('body'),
                ),
                (
                    'category', _(u'Category'), request.get('category'),
                    'list',
                    [(v, v) for v in NoosferoCategory.objects.values_list(
                     'name', flat=True)]
                ),
            )
        },
        'software_community': {
            'name': _(u'Software Community'),
            'icon': 'folder-open',
            'fields': (
                ('finality', _(u'Finality'), request.get('finality')),
                ('features', _(u'Features'), request.get('features')),
                ('tags', _(u'Tags'), request.get('tags')),
            )
        },
    }
