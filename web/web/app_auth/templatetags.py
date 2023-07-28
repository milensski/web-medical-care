from django import template

register = template.Library()


@register.filter(name='check_group')
def has_group(user):
    return user.groups.get.first()
