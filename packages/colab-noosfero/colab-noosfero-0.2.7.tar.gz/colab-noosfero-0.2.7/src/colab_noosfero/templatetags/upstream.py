from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

register = template.Library()


def get_path(link):
    return reverse('noosfero:noosfero', kwargs={'path': link.lstrip('/')})


def get_default_image_url(size):
    return "/images/icons-app/community-{}.png".format(size)


@register.simple_tag(takes_context=True)
def get_image_link_url(context, link, size):
    request = context['request']
    if not link:
        link = get_default_image_url(size)
    return request.build_absolute_uri(get_path(link))


@register.simple_tag()
def get_author(username):
    if username == '':
        return ''
    else:
        profile = reverse('user_profile', kwargs={'username': username})
        return _("By") + ' <a href="%s">%s</a>' % (profile, username)
