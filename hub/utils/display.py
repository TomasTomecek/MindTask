# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import Context, loader
from django.core.exceptions import ObjectDoesNotExist



__all__ = (
    'display_items',
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