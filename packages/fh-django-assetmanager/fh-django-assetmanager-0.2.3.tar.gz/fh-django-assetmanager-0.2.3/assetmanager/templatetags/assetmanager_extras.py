from django import template

register = template.Library()


'''
TODO This is generic enough it should probably
be put in our django common stuff
'''
@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()
