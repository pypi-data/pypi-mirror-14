from django import template

register = template.Library()

@register.filter
def is_in(key, dict):
    return key in dict

@register.filter
def get(dict, key):
    return dict[key]

@register.filter
def items(dict, key):
    return dict[key].items()

@register.filter
def is_dict(obj, key):
    return type(obj[key]) is dict

@register.filter
def is_list(obj, key):
    return type(obj[key]) is list