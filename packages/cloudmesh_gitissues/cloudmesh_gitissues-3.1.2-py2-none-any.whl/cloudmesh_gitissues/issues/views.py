from __future__ import unicode_literals
from __future__ import print_function
from pprint import pprint
import json

from django.shortcuts import render
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.util import banner, path_expand
from  ..settings  import REPOSITORIES

from ..views import dict_table, list_table, list_table_plain, list_table_html5
from ..GitPriority import GitPriority

def url(msg, link):
    print (locals())
    data = {
        'msg': msg,
        'link': link
    }
    return '<a href="{link}"> {msg} </a>'.format(**data)


def issue_list_all(request):

    all_issues = []
    for label, username, repository in REPOSITORIES:
        print ("Loading ... {}/{}".format(username, repository))
        try:
            git = GitPriority(username, repository)
            git.get()
            # print (len(git.issues))
            git.sanitize(username, repository)
            data = git.issues
            order = git.order
            if data is not None:
                all_issues = all_issues + data
        except Exception as e:
            print (e)

    print (order)

    return (list_table_plain(request,
                       title="Issues All",
                       data=all_issues,
                       location="All",
                       order=order,
                       repos=REPOSITORIES))

def issue_list(request, username=None, repository=None):

    print ("Loading ... ", username, repository)
    if username is None or repository is None:
        return issue_list_all(request)
    else:
        git = GitPriority(username, repository)
        git.get()
        git.sanitize(username, repository)

        order = git.order
        location="{}/{}".format(username, repository)
        data = git.issues
        print ("{} {}".format(location, len(git.issues)))
        
        return (list_table_plain(request,
                           title="Issues {}".format(location),
                           data=data,
                           location="{}/{}".format(username, repository),
                           order=order,
                           repos=REPOSITORIES))

def issue_list_html5(request, username=None, repository=None):

    git = GitPriority(username, repository)
    git.get()
    git.sanitize(username, repository)

    order = git.order
    location="{}/{}".format(username, repository)
    data = git.issues

    pprint (REPOSITORIES)

    return (list_table_html5(request,
                       title="Issues {}".format(location),
                       data=data,
                       location="{}/{}".format(username, repository),
                       order=order,
                       repos=REPOSITORIES))




