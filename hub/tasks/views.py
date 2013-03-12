#register xmlrpc methods
import kobo.django.xmlrpc.views

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from models import Task, Stream, UserProfile, MindMap

from utils.display import display_items
#from utils.constants import PROGRESS


@login_required(login_url='/registration/login/')
def task_list(request, stream_name="active", mmap="all", sheet="all",
              order_by="progress", order="up"):
    """
    TODO
        add here filters:
            all
    """
    user = get_object_or_404(UserProfile,user__id=request.user.id)
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
                                stream=stream,
                                sheet__mind_map__user=user)

    if mmap != 'all':
        tasks = tasks.filter(sheet__mind_map__id=mmap)

    if sheet != 'all':
        tasks = tasks.filter(sheet__id=sheet)

    if order_by != 'color':
        tasks = tasks.order_by(o)
    else:
        tasks_list = list(tasks)
        rev = False
        if order == 'down':
            rev=True
        tasks_list.sort(key=lambda x: x.color_value(), reverse=rev)
        tasks = tasks_list

    return render_to_response(
        "task_list.html",
        {
            'task_list': mark_safe(display_items(tasks)),
            'streams': Stream.objects.all(),
            'stream': stream,
            'order': order,
            'current_map': mmap,
            'current_sheet': sheet,
            'maps': MindMap.objects.filter(user=user)
        },
        context_instance=RequestContext(request)
    )
