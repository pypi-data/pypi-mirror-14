Github Issues with Priorities
=======================================

Github does not provide natively the support of priorities for issues.
Cloudmesh Github Issues introduces a simple way to do so while not using
labels, but by augmenting the issue boddy.

We provide a simple django bootstrap based portal interface that looks
into the github issues and finds in the first line of an isse the
priority defined with::

  P:10

where 10 is the priority. If no priority is given we use 999
indicating a low priority.


Install
--------

The install requires an install from github so you are up to date and
get all needed files. If you download the packae from pypi, we
recommend that you do the github instalation instead. We also
typically recommend using virtualenv.

::

    mkdir -p ~/github/cloudmesh
    cd ~/github/cloudmesh
    git clone https://github.com/cloudmesh/gitissues.git
    pip install -r requirements.txt
    python setup.py install

Customization
-------------

In `cloudmesh_gitissues/settings.py` change the list of repositories that
you like to include::

    REPOSITORIES = [
        ("Client", "cloudmesh", "client"),
        ("Portal", "cloudmesh", "portal"),
        ("Workflow", "cloudmesh", "workflow"),
        ("Yubikey", "cloudmesh", "yubikey"),
        ("Big Data Stack", "futuresystems" "big-data-stack"),
        ]

Each entry has the form::

    (Label, git_username, git_repository)

For example the entry for::

    https://github.com/cloudmesh/client

is::

    ("Client", "cloudmesh", "client")

A menu entry will be created for each repository with the given label.

Run portal
-----------

make run

View portal 
-------------

make view

Bugs and enhancement suggestion
--------------------------------

* We should be able to modify the priorities in the table, and have
  a save button that than updates all issues (anyone wants to help?)
