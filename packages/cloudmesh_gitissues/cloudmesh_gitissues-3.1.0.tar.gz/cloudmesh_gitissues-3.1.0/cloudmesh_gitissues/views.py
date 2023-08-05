# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaulttags import register
from sqlalchemy.orm import sessionmaker
from django_jinja import library


# noinspection PyPep8Naming
def Session():
    from aldjemy.core import get_engine
    engine = get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()


session = Session()


@library.global_function
def icon(name, color=None):
    if color is None:
        start = ""
        stop = ""
    else:
        start = '<font color="{}">'.format(color)
        stop = '</font>'
    if name in ["trash"]:
        icon_html = '<i class="fa fa-trash-o"></i>'
    elif name in ["cog"]:
        icon_html = '<i class="fa fa-cog"></i>'
    elif name in ["cog"]:
        icon_html = '<i class="fa fa-info"></i>'
    elif name in ["off"]:
        icon_html = '<i class="fa fa-power-off"></i>'
    elif name in ["on"]:
        icon_html = '<i class="fa fa-power-off"></i>'
    elif name in ["refresh"]:
        icon_html = '<i class="fa fa-refresh"></i>'
    elif name in ["chart"]:
        icon_html = '<i class="fa fa-bar-chart"></i>'
    elif name in ["desktop", "terminal"]:
        icon_html = '<i class="fa fa-desktop"></i>'
    elif name in ["info"]:
        icon_html = '<i class="fa fa-info-circle"></i>'
    elif name in ["launch"]:
        icon_html = '<i class="fa fa-rocket"></i>'
    else:
        icon_html = '<i class="fa fa-question-circle"></i>'
    return start + icon_html + stop


@library.global_function
def state_color(state):
    if state.lower() in ["r", "up", "active", 'yes', 'true']:
        return '<span class="label label-success"> {} </span>'.format(state)
    elif state.lower() in ["down", "down*", "fail", "false"]:
        return '<span class="label label-danger"> {} </span>'.format(state)
    elif "error" in str(state):
        return '<span class="label label-danger"> {} </span>'.format(state)
    else:
        return '<span class="label label-default"> {} </span>'.format(state)


def message(msg):
    return HttpResponse("Message: %s." % msg)


# noinspection PyUnusedLocal
def cloudmesh_vclusters(request):
    return message("Not yet Implemented")


@register.filter
def get_item(dictionary, key):
    value = dictionary.get(key)
    if value is None:
        value = "-"
    return value


def dict_table(request, **kwargs):
    context = kwargs
    #pprint(context)
    return render(request, 'cloudmesh_gitissues/dict_table.jinja', context)

def list_table(request, **kwargs):
    context = kwargs
    #pprint(context)
    return render(request, 'cloudmesh_gitissues/list_table.jinja', context)

def list_table_plain(request, **kwargs):
    context = kwargs
    #pprint(context)
    return render(request, 'cloudmesh_gitissues/list_table_plain.jinja', context)


def homepage(request):
    context = {
        'title': "Github Issues"
    }
    return render(request,
                  'cloudmesh_gitissues/home.jinja',
                  context)
