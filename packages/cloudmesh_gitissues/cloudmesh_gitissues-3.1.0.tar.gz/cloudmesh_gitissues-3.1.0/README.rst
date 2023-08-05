CLoudmesh Github Issues
========================

Although github provides through the label mechnism a
potential for priority management of issues, we sometimes need
to define a much more precise way of doing ordering the priorities
rather than by label groups.

To be able to do that We provide a simple bootstrap based portal
interface that looks into the github issues and finds in the first
line of an isse the priority defined with::

  P:10

where 10 is the priority. If no priority is given we use 999.


Install
--------

::

    mkdir -p ~/github/cloudmesh
    cd ~/github/cloudmesh
    git clone https://github.com/cloudmesh/gitissues.git
    pip install -r requirements.txt
    python setup.py install

Run portal
-----------

make run

View portal 
-------------

Make view

Bugs
-------------