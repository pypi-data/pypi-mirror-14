from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.assignment_tag()
def profile_url(username):
    if not username:
        return ""

    html = '- <a href="%s">%s</a>' % (reverse('user_profile',
                                              kwargs={'username': username}),
                                      username)
    return html
