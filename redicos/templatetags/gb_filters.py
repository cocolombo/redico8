from django.template.defaultfilters import stringfilter
from django import template
import pdb

register = template.Library()

@register.filter(name='abstention')
@stringfilter
def abstention(value):
    value = value.replace(',','.')
    # print(value)
    # print(float(value))
    if float(value) < 0:
        return 'abs'
    else:
        return value
    # print(f'value: {value}')
    # try:
    #     if float(value.replace(',','.')) < 0:
    #         return 'abs'
    #     else:
    #         return u"%s\n" % (value)
    # except:
    #     return u"%s\n" % (value)



# @register.filter(name='get_item')
# def get_item(dict_data, key):
    # usage example {{ your_dict|get_value_from_dict:your_key }}
    # print(f'dict_data: {dict_data}')
    # print(f'key: {key}')
    # print(f'dict_data.get(key): {dict_data.get(key)}')
    # return dict_data.get(key)

@register.filter(name='get_attr')
def get_attr(object, name):
    return getattr(object, name, '')
