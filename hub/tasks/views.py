#register xmlrpc methods
import kobo.django.xmlrpc.views

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required

from models import Task, Stream

from utils.display import display_items
#from utils.constants import PROGRESS


@login_required(login_url='/registration/login/')
def task_list(request, stream_name, order_by, order):
    """
    TODO
        add here filter also:
            all
            completed
            active
    """
    if order == "up":
        o = order_by
        order = "down"
    elif order == "down":
        o = "-%s" % order_by
        order = "up"
    else:
        raise RuntimeError("invalid order")
    stream = Stream.objects.get(name=stream_name)
    tasks = Task.objects.filter(object_id__isnull=True,
                                stream=stream).order_by(o)

    return render_to_response(
        "task_list.html",
        {
            'task_list': mark_safe(display_items(tasks)),
            'streams': Stream.objects.all(),
            'stream': stream,
            'order': order,
        },
        context_instance=RequestContext(request)
    )
