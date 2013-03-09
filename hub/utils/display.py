# -*- coding: utf-8 -*-

import cPickle as pickle

from django.http import HttpResponse
from django.template import Context, loader
from django.core.exceptions import ObjectDoesNotExist

from tasks.models import MindMap, Sheet


__all__ = (
    'display_items',
#    'maps_by_user',
)


def display_items(model_list, level=0):
    html_list = u""

    for model in model_list:
        try:
            model = model.task
        except ObjectDoesNotExist:
            model = model.comment
        template = loader.get_template('list_item.html')
        context = Context({
            'model': model,
            'indent': level,
        })
        content = HttpResponse(template.render(context)).content
        children = model.children()
        html_list += content

        html_list += display_items(children, level+2)
    return html_list


"""
def maps_by_user(user_profile):
    maps = []
    for m in MindMap.objects.filter(user=user_profile):
        map_entry = {}
        map_entry['name'] = m.filename
        map_entry['sheets'] = []
        for s in Sheet.objects.filter(mind_map=m):
            sheet = {}
            sheet['name'] = s.title
            map_entry['sheets'].append(sheet)
        maps.append(map_entry)
    return maps
"""