#register xmlrpc methods
import kobo.django.xmlrpc.views

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe

from models import Task

from utils.display import display_items
from utils.constants import PROGRESS


def task_list(request, query):
    return render_to_response(
        "task_list.html",
        {
            'task_list': mark_safe(display_items(query)),
        },
        context_instance=RequestContext(request)
    )


def task_list_in_progress(request):
    tasks = Task.objects.filter(object_id__isnull=True).\
        exclude(progress=PROGRESS['COMPLETED']).order_by('progress')
    return task_list(request, tasks)


def task_list_completed(request):
    tasks = Task.objects.filter(object_id__isnull=True,
                                progress=PROGRESS['COMPLETED']).\
                                order_by('progress')
    return task_list(request, tasks)