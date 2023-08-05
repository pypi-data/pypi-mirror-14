LibrePlanet schedule generator
==============================

Installation
------------

On a Debian based distribution, do::

  # aptitude install virtualenv python-setuptools

Install globally
~~~~~~~~~~~~~~~~

::

   $ sudo pip install lpschedule-generator


Install locally using virtualenv (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make a separate ``lpschedule-generator`` directory and initialize the
virtual environment in it::

  $ mkdir lpschedule-generator
  $ cd lpschedule-generator

  $ virtualenv .
  $ source bin/activate

Install ``lpschedule-generator`` inside this directory using ``pip``::

  $ pip install lpschedule-generator

Activating virtual environment
``````````````````````````````

Always activate the virtual environment before using the ``lps_gen``
command::

   $ cd path/to/lpschedule-generator
   $ source bin/activate


LP schedule
-----------

LP schedule usage
~~~~~~~~~~~~~~~~~
::

   $ lps_gen -s path/to/lp-sch.jinja2 path/to/lp-sch.md > path/to/program-schedule.html

or::

  $ lps_gen --schedule path/to/lp-schedule.jinja2 path/to/lp-sch.md > path/to/program-schedule.html


LP schedule markdown structure
``````````````````````````````

Overall structure::

   ## Day 1

   ### Timeslot 1

   #### Session 1

   #### Session 2

   ...

   ### Timeslot 2

   #### Session 1

   #### Session 2

   ...

   ## Day 2

   ### Timeslot 1

   #### Session 1

   #### Session 2

   ...

Level two heading (``##``) format::

  ## Saturday, March 19

  ...

  ## Sunday, March 20

Level three heading (``###``) format::

  ### 09:00 - 09:45: Registration and Breakfast

  ### 09:45 - 10:45: Opening Keynote

  ...

  ### 10:55 - 11:40: Session Block 1A

Session structure::

  #### Fork and ignore: fighting a GPL violation by coding instead

  [Bradley Kuhn][kuhn], [Karen Sandler][sandler]

  Room 32-155

  Typically, GPL enforcement activity involves copyright infringement
  actions which compel license violators to correct errors in their
  GPL compliance, defending the policy goals of the GPL: the rights of
  developers and users to copy, share, modify and redistribute.

  While traditional enforcement is often undeniably necessary for
  embedded electronics products, novel approaches to GPL violations
  are often possible and even superior for more traditional software
  distributions.

  Recently, [Software Freedom Conservancy][sfc] engaged in an
  enforcement action whereby, rather than fight the violator in court,
  we instead provided resources and assistance to a vetted
  GPL-compliant fork of a violating codebase.

  This talk discusses which scenarios make this remedy optimal and the
  lessons learned. The talk includes some licensing and technical
  content about vetting the licensing information of codebases.

  [kuhn]: https://libreplanet.org/YEAR/path/to/speakers.html#kuhn
  [sandler]: https://libreplanet.org/YEAR/path/to/speakers.html#sandler
  [sfc]: https://sfconservancy.org/

Sample: https://notabug.org/rsd/lpschedule-generator/raw/dev/tests/files/lp-sch.md


Auto-linking speaker names
++++++++++++++++++++++++++

Speakers in the schedule MD can be auto-linked to speakers' page by
marking them up like this ``[John Hacker]()``

The script converts:

- ``[John Hacker]()`` to ``<a href="speakers.html#hacker">John
  Hacker</a>`` if John Hacker's bio is available in the speakers' page.

- ``[John Hacker]()`` to ``John Hacker`` if John Hacker's bio is not
  available in the speakers' page. In this case, the script also appends
  ``John Hacker`` name in the ``speakers.noids`` file.

  The ``speakers.noids`` file contains a list of speakers who were
  auto-linked in the schedule MD but who's bio is not (yet) available
  in the speakers' page.

For auto-linking speakers, the script uses the ``speakers.ids`` file;
this file is written to the disk after generating the the speakers'
page from MD. Generate the speakers' page before generating the
schedule page for auto-linking to work.

Sample: https://notabug.org/rsd/lpschedule-generator/raw/dev/tests/files/lp-sessions-autolink.md

Special cases
+++++++++++++

Room TBA
........

When a room for a session is not yet available put ``RoomTBA`` as the
placeholder in the line that usually contains the room number; the
rendered HTML will not have the room number for sessions that have
``RoomTBA``.

Sessions only schedule
......................

It is possible to have a sessions only schedule. To do this, at the
beginning of the markdown document:

- Add a level two heading (``##``) with one or more whitespaces.
- Add a level three heading (``###``) with one or more whitespaces.

Sessions only sample: https://notabug.org/rsd/lpschedule-generator/raw/dev/tests/files/lp-sch-sessions-only.md


LP schedule iCal export
~~~~~~~~~~~~~~~~~~~~~~~

The ``--ical`` switch enables iCal export while generating LP
schedule::

  $ lps_gen -s --ical 2016 path/to/lp-schedule.jinja2 path/to/lp-schedule.md > path/to/program-schedule.html

The year of the conference must be given as an argument to the
``--ical`` switch.


LP speakers
-----------

LP speakers usage
~~~~~~~~~~~~~~~~~
::

   $ lps_gen -sp path/to/lp-speakers.jinja2 path/to/lp-speakers.md > path/to/speakers-content.html

or::

  $ lps_gen --speakers path/to/lp-speakers.jinja2 path/to/lp-speakers.md > path/to/speakers-content.html

LP speakers markdown structure
``````````````````````````````

::

   # Keynote speaker name 1

   ![Keynote speaker name 1 - Photo](//fsf.org/images/ks1.jpg)

   Lorem ipsum dolor sit amet keynote speaker 1 bio; can contain
   inline HTML.

   # Keynote speaker name 2

   ![Keynote speaker name 2 - Photo](//fsf.org/images/ks2.jpg)

   Lorem ipsum dolor sit amet keynote speaker 2 bio; can contain
   inline HTML.

   ...

   ## Speaker name 1

   ![Speaker name 1 - Photo](//fsf.org/images/s1.jpg)

   Lorem ipsum dolor sit amet speaker 1 bio; can contain inline HTML.

   ## Speaker name 2

   ![Speaker name 2 - Photo](//fsf.org/images/s2.jpg)

   Lorem ipsum dolor sit amet speaker 2 bio; can contain inline HTML.

   ...


Everything except the speaker name is optional.

Sample: https://notabug.org/rsd/lpschedule-generator/raw/dev/tests/files/lp-speakers.md

Speaker's ID generation
+++++++++++++++++++++++

The last name of the speaker is automatically made the ID; if a
speaker' name is "John Hacker", the ID for this speaker will be
``hacker``.

- If two or more speakers have the same last name, then, the first
  speaker will have their last name as their ID and from the second to
  the n^th speaker will have their full name as their ID; if "Bill
  Hacker" and "Jill Hacker" are two speakers, "Bill" will get
  ``hacker`` as his ID and "Jill" will get ``jill_hacker`` as her ID.

- The IDs are transliterated to ASCII; if a speaker' name is "John
  HÖcker", the ID for this speaker will be ``hacker``.

General
-------

Commenting
~~~~~~~~~~

The markdown files can have comments in the `following three formats`__::

  [comment]: <> (This is one type of comment.)
  [//]: <> (This is another type of comment.)
  [//]: # (This is the third type of comment.)

The comments won't make it to the generated HTML.

.. _md_comments: https://stackoverflow.com/questions/4823468/comments-in-markdown
__ md_comments_

Source
------

::

   $ git clone https://notabug.org/rsd/lpschedule-generator.git


