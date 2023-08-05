from __future__ import unicode_literals
from __future__ import print_function
from pprint import pprint
import json

from django.shortcuts import render
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.util import banner, path_expand


from ..views import dict_table, list_table, list_table_plain
from ..GitPriority import GitPriority

def url(msg, link):
    print (locals())
    data = {
        'msg': msg,
        'link': link
    }
    return '<a href="{link}"> {msg} </a>'.format(**data)


def issue_list(request, username=None, repository=None):

    git = GitPriority(username, repository)
    git.get()
    git.sanitize()

    order = git.order
    location="{}/{}".format(username, repository)
    data = git.issues

    return (list_table_plain(request,
                       title="Issues {}".format(location),
                       data=data,
                       location="{}/{}".format(username, repository),
                       order=order))



