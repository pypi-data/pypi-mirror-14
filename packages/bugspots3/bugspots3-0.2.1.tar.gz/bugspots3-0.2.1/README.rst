bugspots
========

What is bugspots?
-----------------

Bugspots is a Python implementation of `the bug prediction algorithm
used at
Google <http://google-engtools.blogspot.com/2011/12/bug-prediction-at-google.html>`__.
It also embed a command-line interface which can be used to list the
"hot spots" of a Git repository.

What is a hot spot?
~~~~~~~~~~~~~~~~~~~

A hot spot is merely a file that is bug-prone.

How does it work?
-----------------

The algorithm is very simple and to the point: it gives each file a
score based on its number of bug-fixing commits and their age, and then
return a descending-ordered list of the files based on their score,
filtering commits that are no longer at ``HEAD``.

What is a bug-fixing commit?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Any commit whose purpose is to fix an issue. They are identified by
message, using `the same pattern as
GitHub <https://github.com/blog/831-issues-2-0-the-next-generation>`__,
which is:

::

    (?i)(fix(e[sd])?|close[sd]?) #[1-9][0-9]*

What is the formula used?
~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: http://goo.gl/Uoave
   :alt: ``\textrm{score}{\left(i\right)}=\sum_{i=0}^n\frac{1}{1+e^{\left(-12t_i+12\right)}}``

where *ti* is the timestamp of the *i*\ th commit, normalized between 0
and 1 (0 being the date of the first commit in the repository and 1
being the date of the last commit in the repository), and *n* is the
number of bug-fixing commits.

Installation
------------

::

    $ pip3 install bugspots3

Command-line usage
------------------

::

    $ bugspots.py -h

Python example
--------------

.. code:: python

    import bugspots
    b = bugspots.Bugspots()
    for hotspot in b.get_hotspots():
        print(" %6.3f %s" % (hotspot.score, hotspot.filename))
